export type Meta = {schema_version: '1.0'; generated_at: string; source: string; revision: string; clean_sha256: string; raw_sha256: string; population: string; period: string; income_period: string; weight: string; n: number; source_url: string; license_status: string};
export type Overview = {n: number; income_mean: number; income_median: number; hours_mean: number; hours_median: number; income_weighted_mean: number; hours_weighted_mean: number; pearson: number; spearman: number; weighted_pearson: number; zero_hours_n: number; zero_income_n: number; income_p99: number; income_max: number; hours_max: number};
export type Group = {key: string; label: string; n: number; income_mean: number; income_median: number; hours_mean: number};
export type Coefficient = {term: string; estimate: number; se: number; t: number; p: number; ci_low: number; ci_high: number};
export type Visuals = {density: {hours:number;lower:number;upper:number;n:number}[]; boxplots: {key:string;label:string;n:number;q1:number;median:number;q3:number;p10:number;p90:number;mean:number}[]; income_cdf: {income:number;share:number}[]; percentiles: {p:number;income:number;hours:number}[]};
export type Diagnostics = {fit_band:{hours:number;income:number;ci_low:number;ci_high:number}[];residual_density:{hours:number;lower:number;upper:number;n:number}[];residual_histogram:{lower:number;upper:number;n:number}[];qq:{theoretical:number;empirical:number}[];covariance:number[][];t_critical:number;df_inference:number;ee_comparison:{method:string;se:number;ci_low:number;ci_high:number}[];residual_mean:number;residual_skew:number;residual_kurtosis:number;cook_histogram:{lower:number;upper:number;n:number}[];rmse:number;mae:number;adjusted_r_squared:number;sse:number;sst:number;ssr:number};
export type Model = {diagnostics:Diagnostics;n: number; clusters: number; households: number; strata: number; r_squared: number; ser: number; x_variance: number; coefficients: Coefficient[]; heteroskedasticity_p: number; cook_flagged_n: number; sensitivity: {n: number; slope: number; ci_low: number; ci_high: number}; residual_spread: {hours: number; n: number; std: number}[]; fitted: {hours: number; income: number}[]};
export type DashboardData = {visuals:Visuals;selection: {label: string; n: number}[]; overview: Overview; groups: Group[]; hours: {hours: number; n: number}[]; income: {label: string; lower: number; upper: number | null; n: number}[]; availability: {label: string; n: number}[]; model: Model};
export type Envelope = {data: DashboardData; meta: Meta};

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
function numbers(value: Record<string, unknown>, keys: string[]) {
  return keys.every(key => typeof value[key] === 'number' && Number.isFinite(value[key]));
}
function rows(value: unknown, check: (row: Record<string, unknown>) => boolean): boolean {
  return Array.isArray(value) && value.every(row => record(row) && check(row));
}
/** Reject malformed aggregates before rendering any statistics. No fallback figures. */
export function isEnvelope(value: unknown): value is Envelope {
  if (!record(value) || !record(value.meta) || !record(value.data)) return false;
  const m = value.meta, d = value.data;
  if (m.schema_version !== '1.0' || !numbers(m, ['n']) || Number(m.n) < 0) return false;
  if (!['generated_at', 'source', 'revision', 'clean_sha256', 'raw_sha256', 'population', 'period', 'income_period', 'weight', 'source_url', 'license_status'].every(k => typeof m[k] === 'string')) return false;
  if (!record(d.visuals) || !record(d.model) || !record(d.model.diagnostics)) return false;
  if (!rows(d.visuals.density,r=>numbers(r,['hours','lower','upper','n']))) return false;
  if (!rows(d.visuals.boxplots,r=>typeof r.key==='string'&&typeof r.label==='string'&&numbers(r,['n','q1','median','q3','p10','p90','mean']))) return false;
  if (!rows(d.visuals.income_cdf,r=>numbers(r,['income','share']))) return false;
  if (!rows(d.visuals.percentiles,r=>numbers(r,['p','income','hours']))) return false;
  const diag=d.model.diagnostics;
  if (!numbers(diag,['t_critical','df_inference','residual_mean','residual_skew','residual_kurtosis','rmse','mae','adjusted_r_squared','sse','sst','ssr'])) return false;
  if (!rows(diag.fit_band,r=>numbers(r,['hours','income','ci_low','ci_high'])) || !rows(diag.residual_density,r=>numbers(r,['hours','lower','upper','n'])) || !rows(diag.residual_histogram,r=>numbers(r,['lower','upper','n'])) || !rows(diag.cook_histogram,r=>numbers(r,['lower','upper','n'])) || !rows(diag.qq,r=>numbers(r,['theoretical','empirical'])) || !rows(diag.ee_comparison,r=>typeof r.method==='string'&&numbers(r,['se','ci_low','ci_high']))) return false;
  if (!Array.isArray(diag.covariance) || diag.covariance.length!==2 || !diag.covariance.every(r=>Array.isArray(r)&&r.length===2&&r.every(v=>typeof v==='number'&&Number.isFinite(v)))) return false;
  if (!record(d.overview) || !record(d.model) || !record(d.model.sensitivity)) return false;
  if (!numbers(d.overview, ['n','income_mean','income_median','hours_mean','hours_median','income_weighted_mean','hours_weighted_mean','pearson','spearman','weighted_pearson','zero_hours_n','zero_income_n','income_p99','income_max','hours_max'])) return false;
  if (!numbers(d.model, ['n','clusters','households','strata','r_squared','ser','x_variance','heteroskedasticity_p','cook_flagged_n'])) return false;
  if (!numbers(d.model.sensitivity, ['n','slope','ci_low','ci_high'])) return false;
  if (!rows(d.model.coefficients, r => typeof r.term === 'string' && numbers(r, ['estimate','se','t','p','ci_low','ci_high']))) return false;
  if (!Array.isArray(d.model.coefficients) || d.model.coefficients.length !== 2) return false;
  if (!rows(d.model.fitted, r => numbers(r, ['hours','income'])) || !rows(d.model.residual_spread, r => numbers(r, ['hours','n','std']))) return false;
  if (!rows(d.selection, r => typeof r.label === 'string' && numbers(r,['n']))) return false;
  if (!rows(d.availability, r => typeof r.label === 'string' && numbers(r,['n']))) return false;
  if (!rows(d.groups, r => typeof r.key === 'string' && typeof r.label === 'string' && numbers(r,['n','income_mean','income_median','hours_mean']))) return false;
  if (!rows(d.hours, r => numbers(r,['hours','n']))) return false;
  if (!rows(d.income, r => typeof r.label === 'string' && numbers(r,['lower','n']) && (r.upper === null || numbers(r,['upper'])))) return false;
  if (d.overview.n !== m.n || d.model.n !== m.n) return false;
  if (Number(m.n) > 0 && (![d.groups,d.hours,d.income,d.selection].every(a => Array.isArray(a) && a.length > 0))) return false;
  if (Array.isArray(d.hours) && d.hours.reduce((s,r) => s + Number(r.n),0) !== m.n) return false;
  if (Array.isArray(d.groups) && d.groups.reduce((s,r) => s + Number(r.n),0) !== m.n) return false;
  if (Array.isArray(d.income) && d.income.reduce((s,r) => s + Number(r.n),0) !== m.n) return false;
  for(const bins of [d.visuals.density,diag.residual_density,diag.residual_histogram,diag.cook_histogram]) {if(!Array.isArray(bins)||bins.some(r=>Number(r.n)<0)||bins.reduce((sum,r)=>sum+Number(r.n),0)!==m.n)return false;}
  if(Number(m.n)>0){for(const collection of [d.visuals.boxplots,d.visuals.income_cdf,d.visuals.percentiles,diag.qq,diag.fit_band,diag.ee_comparison])if(!Array.isArray(collection)||collection.length===0)return false;}
  if(Array.isArray(d.visuals.income_cdf)&&d.visuals.income_cdf.some(r=>Number(r.share)<0||Number(r.share)>1))return false;
  if(Array.isArray(diag.fit_band)&&diag.fit_band.some(r=>Number(r.ci_low)>Number(r.ci_high)))return false;
  return true;
}
