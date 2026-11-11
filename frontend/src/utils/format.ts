export const pct=(v:unknown)=>{const n=Number(v||0);return n>.9999&&n<1?">99.99%":(n*100).toFixed(2)+"%"};export const integer=(v:unknown)=>Number(v||0).toLocaleString("zh-CN");
export const detectionPct=(v:unknown,guaranteed=false)=>guaranteed?"100.00%":Number(v)>=.9999?">99.99%":pct(v);
