import sys
from pypdf import PdfReader, PdfWriter


def main():
    file = sys.argv[1]
    reader = PdfReader(file)
    writer = PdfWriter()

    page = reader.pages[0]
    page.mediabox.lower_right = (
        page.mediabox.right,
        page.mediabox.top / 2,
    )

    page.rotate(90)

    writer.add_page(page)

    with open("output.pdf", "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    main()
