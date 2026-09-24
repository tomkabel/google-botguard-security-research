"""Print the body page count (pages before the References heading) against the S&P SoK limit of 13."""
import subprocess, sys

pdf = sys.argv[1]
n = int(next(l.split()[-1] for l in subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")))
ref = next(i for i in range(1, n + 1) if "\nReferences\n" in "\n" + subprocess.run(
    ["pdftotext", "-f", str(i), "-l", str(i), pdf, "-"], capture_output=True, text=True).stdout)
print(f"{n} pages total; References start on page {ref} (body limit 13, total limit 18)")
