Cloudflare just pulled Chrome, Edge and Firefox into one anti-bot protocol: 𝗣𝗔𝗖𝗧 (𝘗𝘳𝘪𝘷𝘢𝘵𝘦 𝘈𝘤𝘤𝘦𝘴𝘴 𝘊𝘰𝘯𝘵𝘳𝘰𝘭 𝘛𝘰𝘬𝘦𝘯𝘴), announced with Mozilla, Google, Microsoft and Shopify, lets a site that already knows a visitor is real issue an anonymous token. The browser carries it to the next site as proof a human is in the loop. No CAPTCHA, no forced login, no fingerprinting. It extends Privacy Pass (RFC 9576) with blind signatures, so the receiving site verifies the token against a public key and learns nothing about who you are.
 
The timing is the tell. Bots now make up roughly 58% of all HTTP requests Cloudflare sees, against 42% from people. The old job was sorting human from bot. That question is dead. The new one is sorting authorized from abusive, and personhood from automation, without tracking anyone to do it.
 
For anyone tracking the agentic trust stack, this slots in cleanly. Web Bot Auth answers "𝘪𝘴 𝘵𝘩𝘪𝘴 𝘷𝘦𝘳𝘪𝘧𝘪𝘢𝘣𝘭𝘺 𝘎𝘰𝘰𝘨𝘭𝘦'𝘴 𝘢𝘨𝘦𝘯𝘵" by having the bot sign its own request. PACT answers "is a real person behind this session" without naming them. Different layers, same stack. An AI assistant shopping for you could carry a valid token and pass; an unauthorized scraper carries nothing and hits the same wall as today.
 
What the announcement does not settle is who gets to mint personhood. Trusted issuer status is the actual power here, and it tends to concentrate. Worth noting Apple sat this one out, despite co-creating Private Access Tokens with Cloudflare in 2022.
 
