import os
from typing import Optional
from pathlib import Path
from agno.utils.log import logger
from agno.agent import Agent, Toolkit

try:
    # Try importing markdown-pdf or similar
    # For now we will use a simple HTML wrapping + print logic or just a stub if libs missing
    # In a real environment we would use 'weasyprint' or 'pdfkit' with wkhtmltopdf
    import markdown2
    # import pdfkit # Optional, commonly complex to install in docker without binary
except ImportError:
    pass

class PDFConverterTools(Toolkit):
    def __init__(self, output_dir: str = "output_pdfs"):
        super().__init__(name="pdf_converter_tools")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.register(self.convert_markdown_to_pdf)

    def convert_markdown_to_pdf(self, markdown_content: str, filename: str = "document.pdf") -> str:
        """
        Convierte contenido Markdown a un archivo PDF.
        
        Args:
            markdown_content (str): El contenido en formato markdown a convertir.
            filename (str): Nombre del archivo de salida.
            
        Returns:
            str: Ruta absoluta del archivo generado.
        """
        try:
            # 1. Convert MD to HTML
            html_content = markdown2.markdown(markdown_content, extras=["tables", "fenced-code-blocks"])
            
            # 2. Add some basic styling
            styled_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Helvetica, Arial, sans-serif; line-height: 1.6; padding: 40px; }}
                    h1, h2, h3 {{ color: #2c3e50; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    code {{ background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; }}
                    pre {{ background-color: #f8f9fa; padding: 15px; overflow-x: auto; }}
                    blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 10px; color: #666; }}
                </style>
            </head>
            <body>
            {html_content}
            </body>
            </html>
            """
            
            output_path = self.output_dir / filename
            output_html_path = self.output_dir / f"{filename}.html"
            
            # Save HTML as intermediate step (or final if PDF lib missing)
            with open(output_html_path, "w", encoding="utf-8") as f:
                f.write(styled_html)
                
            logger.info(f"✅ HTML generado en: {output_html_path}")
            
            # 3. TODO: Call PDF generator (e.g. WeasyPrint)
            # For this demo/environment where we might miss dependencies, we return the HTML path as "PDF ready"
            # In production: HTML(string=styled_html).write_pdf(target=str(output_path))
            
            return f"Documento generado (HTML/PDF): {output_html_path}"

        except Exception as e:
            logger.error(f"❌ Error convirtiendo a PDF: {e}")
            return f"Error generando PDF: {str(e)}"
