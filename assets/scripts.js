var opt = {
    margin:       0,
    filename:     'myfile.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 3 },
    jsPDF:        { unit: 'mm', format: 'tabloid', orientation: 'l', floatPrecision: 'smart' }
  };

function printPDF(){
    const button = document.getElementById("descargar-reporte")
    console.log(button)
    
    if (button) {
        button.addEventListener('click', () => {
            html2pdf(document.body, opt)
        });
      }
}
setTimeout(printPDF,500)