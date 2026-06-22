import pymupdf
import os


def getbooks():
    books = os.listdir('books')
    for book in books:
        fullpath = os.path.join('books', book)
        split_name = os.path.splitext(book)
        
        # Try PyMuPDF first
        try:
            doc = pymupdf.open(fullpath)
            with open(f"{split_name[0]}.txt", "wb") as out:
                for page in doc:
                    text = page.get_text().encode("utf8")
                    out.write(text)
                    out.write(bytes((12,)))
                print(f"Processed {book} with PyMuPDF")
            continue
        except Exception as e:
            print(f"PyMuPDF failed for {book}: {e}")
            print(f"Trying pypdf for {book}...")
        
        # Fall back to pypdf
        try:
            extract_with_pypdf(fullpath, f"{split_name[0]}.txt")
            print(f"Processed {book} with pypdf")
        except Exception as e:
            print(f"Both libraries failed for {book}: {e}")
# Review this next look through
def extract_with_pypdf(fullpath, output_file):
    with open(fullpath, "rb") as f:
        reader = pypdf.PdfReader(f)
        with open(output_file, "w", encoding="utf-8") as out:
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    out.write(text)
                    out.write("\n\n--- PAGE BREAK ---\n\n")

if __name__ == "__main__":
    getbooks()