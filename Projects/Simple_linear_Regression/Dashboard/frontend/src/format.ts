export const count=(n:number)=>new Intl.NumberFormat('es-EC',{maximumFractionDigits:0}).format(n);
export const fmt=(n:number,d=2)=>Math.abs(n)>=1e12?n.toExponential(Math.min(d,6)).replace('.',','):new Intl.NumberFormat('es-EC',{minimumFractionDigits:d,maximumFractionDigits:d}).format(n);
export const usd=(n:number,d=0)=>`USD ${fmt(n,d)}`;
export const pct=(n:number,d=1)=>`${fmt(100*n,d)} %`;
export const pvalue=(n:number)=>n<.0001?n.toExponential(2).replace('.',','):fmt(n,4);
export const compact=(n:number)=>Math.abs(n)>=1000?`${fmt(n/1000,Math.abs(n)%1000===0?0:1)}k`:fmt(n,Number.isInteger(n)?0:1);
export const colors=['#305be8','#08a3b8','#8461d9','#e87361','#0b947e'];
