import { test, expect } from '@playwright/test';
import { readFileSync, mkdirSync } from 'node:fs';
import AxeBuilder from '@axe-core/playwright';
const artifact=JSON.parse(readFileSync(new URL('../public/data/dashboard.json',import.meta.url),'utf8'));
const evidence=new URL('../../docs/evidence/v2/',import.meta.url).pathname;
const nav=(page:import('@playwright/test').Page,view:string)=>page.locator(`nav a[href="#${view}"]`);
async function ready(page:import('@playwright/test').Page){await expect(page.getByTestId('density-chart')).toBeVisible();}
const number=(value:number)=>new Intl.NumberFormat('es-EC',{minimumFractionDigits:2,maximumFractionDigits:2}).format(value);

for(const width of [360,390,430,768,1024,1536,1920]){
 test(`tres vistas sin desbordamiento a ${width}px`,async({page})=>{
  const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
  await page.setViewportSize({width,height:1000});await page.goto('/');await ready(page);
  for(const view of ['explorar','modelo','datos']){
   await nav(page,view).click();
   await expect(nav(page,view)).toHaveAttribute('aria-current','page');
   expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
   if(view==='modelo')await expect(page.getByTestId('fit-chart')).toBeVisible();
   if(view==='datos')await expect(page.getByTestId('data-table')).toBeVisible();
  }
  expect(errors).toEqual([]);
 });
}

test('marca, autores, modo claro y EDA con cinco gráficos',async({page})=>{
 await page.setViewportSize({width:1536,height:1000});
 await page.emulateMedia({colorScheme:'dark'});
 await page.addInitScript(()=>localStorage.setItem('cristal-theme','dark'));
 await page.goto('/');await ready(page);
 await expect(page.locator('body')).not.toContainText('Cristal');
 await expect(page.locator('header')).toContainText(/grupo\s*2/i);
 for(const author of ['Jefferson Cueva','Giorge Steven','Jenifer Fernandez'])await expect(page.locator('footer')).toContainText(author);
 expect(await page.locator('html').evaluate(el=>getComputedStyle(el).colorScheme)).toBe('light');
 for(const id of ['density-chart','hours-chart','income-chart','boxplot-chart','cdf-chart'])await expect(page.getByTestId(id)).toBeVisible();
 // Pantalla ocupada, no columna estrecha en escritorio.
 const main=await page.locator('main').boundingBox();
 expect(main!.width).toBeGreaterThan(1000);
 await expect(page.getByRole('button',{name:/modo oscuro|modo claro/i})).toHaveCount(0);
});

test('fórmulas KaTeX locales y diagnóstico gráfico técnico',async({page})=>{
 const failed:string[]=[];page.on('requestfailed',r=>failed.push(r.url()));
 await page.goto('/#modelo');
 await expect(page.getByTestId('fit-chart')).toBeVisible();
 expect(await page.locator('.katex math').count()).toBeGreaterThanOrEqual(2);
 await expect(page.locator('.katex-error')).toHaveCount(0);
 for(const id of ['residual-density','residual-histogram','qq-chart'])await expect(page.getByTestId(id)).toBeVisible();
 await expect(page.locator('body')).toContainText('61,356');
 await expect(page.locator('body')).toContainText('3,747');
 await expect(page.locator('body')).toContainText(/UPM/);
 await expect(page.locator('body')).toContainText(/causal/i);
 await page.evaluate(()=>document.fonts.ready);
 expect(failed).toEqual([]);
});

test('escenario positivo, negativo, cero y extrapolación',async({page})=>{
 await page.goto('/#modelo');await expect(page.getByTestId('scenario-x0')).toBeVisible();
 const x0=page.getByTestId('scenario-x0'),x1=page.getByTestId('scenario-x1');
 const slope=artifact.data.model.coefficients[1];
 async function scenario(a:number,b:number){await x0.fill(String(a));await x0.blur();await x1.fill(String(b));await x1.blur();}
 await scenario(3,6);
 await expect(page.getByTestId('scenario-delta')).toContainText(number(3*slope.estimate));
 await expect(page.getByTestId('scenario-ci')).toContainText(number(3*slope.ci_low));
 await expect(page.getByTestId('scenario-ci')).toContainText(number(3*slope.ci_high));
 await scenario(8,2);
 await expect(page.getByTestId('scenario-delta')).toContainText(number(-6*slope.estimate));
 await expect(page.getByTestId('scenario-ci')).toContainText(number(-6*slope.ci_high));
 await expect(page.getByTestId('scenario-ci')).toContainText(number(-6*slope.ci_low));
 await scenario(4,4);await expect(page.getByTestId('scenario-delta')).toContainText('0,00');
 await scenario(3,24);await expect(page.getByTestId('extrapolation-warning')).toBeVisible();
 await expect(page.getByTestId('scenario-x1')).toHaveValue('24');
 await scenario(3,6);await expect(page.getByTestId('extrapolation-warning')).toHaveCount(0);
});

test('datos agregados, búsqueda y descarga CSV real',async({page})=>{
 await page.goto('/#datos');await expect(page.getByTestId('data-table')).toBeVisible();
 const initial=await page.getByTestId('data-table').locator('tbody tr').count();expect(initial).toBeGreaterThan(0);
 const search=page.getByTestId('data-search');await search.fill('NO_EXISTE_2026');
 await expect.poll(()=>page.getByTestId('data-table').locator('tbody tr').count()).toBeLessThan(initial);
 await search.fill('');
 const downloadPromise=page.waitForEvent('download');await page.getByTestId('download-csv').click();
 const download=await downloadPromise;expect(download.suggestedFilename()).toMatch(/\.csv$/);
 const path=await download.path();const text=readFileSync(path!,'utf8');
 expect(text.length).toBeGreaterThan(50);
 for(const field of ['id_persona','id_hogar','id_vivienda','ingrl_original'])expect(text).not.toContain(field);
});

test('carga, error recuperable y fuente malformada',async({page})=>{
 let failure=true;
 await page.route('**/data/dashboard.json',route=>failure?route.fulfill({status:503,body:'{}'}):route.fulfill({json:artifact}));
 await page.goto('/');await expect(page.getByRole('alert')).toBeVisible();
 await expect(page.getByTestId('density-chart')).toHaveCount(0);
 failure=false;await page.getByRole('button',{name:/reintentar|volver a intentar/i}).click();await ready(page);
 await page.unroute('**/data/dashboard.json');
 await page.route('**/data/dashboard.json',route=>route.fulfill({json:{meta:{schema_version:'1.0',n:9881},data:{}}}));
 await page.reload();await expect(page.getByRole('alert')).toBeVisible();
});

test('teclado y reduced-motion',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');await ready(page);
 await page.keyboard.press('Tab');const skip=page.getByRole('link',{name:/saltar al contenido/i});
 await expect(skip).toBeFocused();await page.keyboard.press('Enter');await expect(page.locator('main')).toBeFocused();
 const animations=await page.locator('main').evaluate(el=>el.getAnimations({subtree:true}).filter(a=>a.playState==='running').length);
 expect(animations).toBe(0);
});

for(const width of [390,1536]){
 test(`accesibilidad de las tres secciones a ${width}px`,async({page})=>{
  await page.setViewportSize({width,height:1000});await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');await ready(page);
  for(const view of ['explorar','modelo','datos']){
   await nav(page,view).click();
   const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
   expect(results.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))).toEqual([]);
  }
 });
 test(`capturas finales a ${width}px`,async({page})=>{
  test.setTimeout(60000);mkdirSync(evidence,{recursive:true});
  await page.setViewportSize({width,height:1000});await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');await ready(page);
  for(const view of ['explorar','modelo','datos']){
   await nav(page,view).click();await page.screenshot({path:`${evidence}${view}-${width}.png`,fullPage:true});
  }
 });
}

test('agregados v2 incompletos se rechazan antes de dibujar',async({page})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 const broken=structuredClone(artifact);broken.data.visuals.income_cdf=[];
 await page.route('**/data/dashboard.json',route=>route.fulfill({json:broken}));
 await page.goto('/');await expect(page.getByRole('alert')).toBeVisible();
 await expect(page.getByTestId('cdf-chart')).toHaveCount(0);expect(errors).toEqual([]);
});

test('el mapa de concentración responde al teclado',async({page})=>{
 await page.goto('/');await ready(page);
 const chart=page.getByTestId('density-chart');
 const previous=await chart.locator('.chart-readout').innerText();
 await chart.locator('svg').focus();await page.keyboard.press('ArrowRight');
 await expect(chart.locator('.chart-readout')).not.toHaveText(previous!);
});

test('comparación entre tramos cambia la medida sin alterar la muestra',async({page})=>{
 await page.goto('/');await ready(page);
 const readout=page.getByTestId('boxplot-chart').locator('.chart-readout');
 const whole=(v:number)=>`USD ${new Intl.NumberFormat('es-EC',{maximumFractionDigits:0}).format(v)}`;
 await expect(readout).toContainText(`Mediana ${whole(artifact.data.visuals.boxplots[0].median)}`);
 await page.getByRole('button',{name:'Promedio',exact:true}).click();
 await expect(readout).toContainText(`Promedio ${whole(artifact.data.visuals.boxplots[0].mean)}`);
 await page.getByRole('button',{name:'Mediana',exact:true}).click();
 await expect(readout).toContainText(`Mediana ${whole(artifact.data.visuals.boxplots[0].median)}`);
 await expect(page.locator('.metrics-grid')).toContainText('9.881');
});
