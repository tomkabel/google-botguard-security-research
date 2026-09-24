-- paper.md -> IEEEtran body. Title/abstract/keywords go to metadata, "## 3. X" becomes a numbered
-- \section (IEEEtran numbers it, so the manual number is dropped), unnumbered headings stay
-- unnumbered, and pipe tables become booktabs tabulars (pandoc's longtable breaks in two columns).
local stringify = pandoc.utils.stringify

local function latex(blocks)
  return (pandoc.write(pandoc.Pandoc(blocks), "latex"):gsub("%s+$", ""))
end

local function tex_table(tbl)
  local rows, width = {}, {}
  local function add(row)
    local cells = {}
    for i, c in ipairs(row.cells) do
      cells[i] = latex(c.contents)
      width[i] = math.max(width[i] or 4, #stringify(c.contents))
    end
    rows[#rows + 1] = cells
  end
  for _, r in ipairs(tbl.head.rows) do add(r) end
  local nhead = #rows
  for _, b in ipairs(tbl.bodies) do for _, r in ipairs(b.body) do add(r) end end
  local total = 0
  for i, w in ipairs(width) do width[i] = math.sqrt(math.min(w, 120)); total = total + width[i] end
  local raw = 0
  for _, w in ipairs(width) do raw = raw + w * w end
  local wide = #width >= 6 or raw > 110 * 110 / 2
  local env = wide and "table*" or "table"
  local spec = {}
  for i, w in ipairs(width) do
    spec[i] = string.format(">{\\raggedright\\arraybackslash\\hspace{0pt}}p{%.3f\\dimexpr\\linewidth-%d\\tabcolsep}", w / total, 2 * #width)
  end
  local out = { "\\begin{" .. env .. "}[t]\\centering\\footnotesize\\setlength{\\tabcolsep}{3pt}" }
  local cap = tbl.caption and tbl.caption.long and latex(tbl.caption.long) or ""
  if cap ~= "" then out[#out + 1] = "\\parbox{\\linewidth}{\\centering " .. cap .. "}\\par\\smallskip" end
  out[#out + 1] = "\\begin{tabular}{@{}" .. table.concat(spec) .. "@{}}\\toprule"
  for i, r in ipairs(rows) do
    out[#out + 1] = table.concat(r, " & ") .. " \\\\" .. (i == nhead and "\\midrule" or "")
  end
  out[#out + 1] = "\\bottomrule\\end{tabular}\\end{" .. env .. "}"
  return pandoc.RawBlock("latex", table.concat(out, "\n"))
end

function Pandoc(doc)
  local meta, body, abstract, mode = doc.meta, {}, {}, nil
  for _, b in ipairs(doc.blocks) do
    if b.t == "Header" and b.level == 1 then
      meta.title = b.content
    elseif b.t == "HorizontalRule" then
      -- drop
    elseif b.t == "Para" and stringify(b):match("^Authors:") then
      -- anonymous author block comes from the template
    elseif b.t == "Para" and stringify(b):match("^Keywords:") then
      local kw = {}
      for k in stringify(b):gsub("^Keywords:%s*", ""):gmatch("[^,]+") do kw[#kw + 1] = pandoc.MetaString((k:gsub("^%s+", ""))) end
      meta.keywords = kw
    elseif b.t == "Header" and stringify(b) == "Abstract" then
      mode = "abstract"
    elseif mode == "abstract" and b.t ~= "Header" then
      abstract[#abstract + 1] = b
    else
      if b.t == "Header" then
        mode = nil
        local num = b.content[1] and b.content[1].t == "Str" and b.content[1].text:match("^%d[%d%.]*$")
        if num then
          b.content = { table.unpack(b.content, 3) }
        else
          b.classes:insert("unnumbered")
        end
        b.level = b.level - 1
        body[#body + 1] = b
        if stringify(b) == "References" then body[#body + 1] = pandoc.RawBlock("latex", "\\footnotesize\\raggedright") end
        if stringify(b):match("^Appendix") then table.insert(body, #body, pandoc.RawBlock("latex", "\\normalsize\\rightskip=0pt\\parfillskip=0pt plus 1fil")) end
      elseif b.t == "Table" then
        body[#body + 1] = tex_table(b)
      elseif b.t == "CodeBlock" then  -- equations: wrap inside the column instead of overflowing it
        body[#body + 1] = pandoc.RawBlock("latex", "\\begin{Verbatim}[fontsize=\\footnotesize,breaklines,breakanywhere]\n" .. b.text .. "\n\\end{Verbatim}")
      else
        body[#body + 1] = b
      end
    end
  end
  meta.abstract = pandoc.MetaBlocks(abstract)
  return pandoc.Pandoc(body, meta)
end
