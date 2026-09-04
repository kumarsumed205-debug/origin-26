import React, { useState } from "react";
import {
  Activity, Bell, CalendarDays, Check, Cloud, CloudSun, Droplets,
  HeartPulse, Info, MapPin, Menu, Moon, Navigation, ShieldCheck,
  Sparkles, Sun, UserRound, Wind
} from "lucide-react";

const EMPTY_DATA = {
  user: { profile: {} }, location: null, weather: null, air_quality: null,
  risk: null, advisory: null, forecast: [], trends: []
};

function readData() { return { ...EMPTY_DATA, ...(window.__CLIMACARE_DATA__ || {}) }; }
function valueOrPlaceholder(value, suffix = "") { return value === null || value === undefined || value === "" ? "--" : `${value}${suffix}`; }
function locationLabel(location) {
  if (!location) return "Location pending";
  if (typeof location === "string") return location;
  return location.name || location.city || location.label || location.display_name || "Location pending";
}
function greeting() { const hour = new Date().getHours(); return hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening"; }
function WeatherIcon({ type = "partly" }) {
  if (type === "sun") return <Sun className="forecast-icon sun" />;
  if (type === "cloud") return <Cloud className="forecast-icon" />;
  return <CloudSun className="forecast-icon" />;
}

function MetricCard({ label, value, unit, icon: Icon, pending }) {
  return <article className="metric-card">
    <div className="metric-head"><Icon size={23} strokeWidth={1.9} /><span>{label}</span></div>
    <div className="metric-value">{valueOrPlaceholder(value)}{unit && <small>{unit}</small>}</div>
    <span className={`status-pill ${pending ? "pending" : "good"}`}>{pending ? "Waiting" : "Current"}</span>
  </article>;
}

function AppHeader({ active, setActive, dark, setDark, location }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const links = ["Home", "Trends", "Profile", "About"];
  return <header className="topbar">
    <div className="brand"><div className="brand-mark"><CloudSun size={25} /></div><div><div className="brand-name">ClimaCare <b>AI</b></div><div className="brand-tagline">Your environment. Your health.</div></div></div>
    <nav className={`nav-links ${mobileOpen ? "open" : ""}`} aria-label="Primary navigation">
      {links.map(link => <button key={link} className={`nav-link ${active === link ? "active" : ""}`} onClick={() => { setActive(link); setMobileOpen(false); }}>{link}</button>)}
    </nav>
    <div className="header-actions"><div className="location-chip"><MapPin size={17} /><span>{locationLabel(location)}</span></div><button className="icon-button" aria-label="Toggle theme" onClick={() => setDark(!dark)}>{dark ? <Sun size={19} /> : <Moon size={19} />}</button><button className="icon-button bell" aria-label="Notifications"><Bell size={19} /></button><button className="avatar" aria-label="Profile" onClick={() => setActive("Profile")}><UserRound size={18} /></button></div>
    <button className="mobile-menu" aria-label="Menu" aria-expanded={mobileOpen} onClick={() => setMobileOpen(!mobileOpen)}><Menu size={23} /></button>
  </header>;
}

function RiskCard({ risk }) {
  const level = risk?.level;
  return <article className={`panel risk-panel ${level ? "risk-provided" : "risk-pending"}`}>
    <div className="panel-title-row"><div className="title-with-icon"><span className="title-icon green"><HeartPulse size={19} /></span><h2>Your Personal Health Risk</h2></div></div>
    <div className="risk-body"><div className="risk-circle"><HeartPulse size={42} /></div><div><div className="risk-level">{level || "Preparing your assessment"}</div><p>{risk?.message || "Your risk assessment will appear once today’s environmental data is ready."}</p></div></div>
    {risk?.detail && <div className="risk-note"><Check size={18} /><span>{risk.detail}</span></div>}
  </article>;
}

function AdvisoryCard({ advisory, risk }) {
  const sections = advisory && typeof advisory === "object" && !Array.isArray(advisory) ? Object.entries(advisory) : null;
  return <article className="panel advisory-panel">
    <div className="panel-title-row"><div className="title-with-icon"><span className="title-icon blue"><Sparkles size={19} /></span><h2>Your Personalized Advisory</h2></div></div>
    {risk?.level && <div className="advisory-risk">Risk: {risk.level}</div>}
    {!advisory && <div className="empty-copy">Your personalized guidance will appear here once today’s environmental data is ready.</div>}
    {typeof advisory === "string" && <div className="advisory-text">{advisory}</div>}
    {sections && <div className="advisory-list">{sections.filter(([, content]) => content != null).map(([title, content]) => <div className="advisory-item" key={title}><span className="advisory-icon"><Activity size={19} /></span><div><strong>{title}</strong><p>{Array.isArray(content) ? content.join(" ") : String(content)}</p></div></div>)}</div>}
  </article>;
}

function ForecastCard({ forecast }) {
  return <article className="panel forecast-panel">
    <div className="panel-title-row"><div className="title-with-icon"><span className="title-icon blue"><CalendarDays size={19} /></span><h2>7-Day Forecast</h2></div></div>
    {!forecast?.length && <div className="empty-copy">Forecast details will appear here when weather data is available.</div>}
    {forecast?.length > 0 && <div className="forecast-list">{forecast.map((item, index) => <div className="forecast-row" key={item.day || index}><span>{item.day || "--"}</span><WeatherIcon type={item.type} /><strong>{item.temperature || item.temp || "--"}</strong></div>)}</div>}
  </article>;
}

function HeroWeather({ location, weather }) {
  return <article className="weather-card"><div className="weather-top"><div className="weather-location"><MapPin size={17} /><span>{locationLabel(location)}</span><span className="updated">{weather?.updated || "Waiting for weather data"}</span></div></div><div className="weather-main"><div><div className="eyebrow">Current weather</div><div className="temperature-line"><strong>{valueOrPlaceholder(weather?.temperature)}</strong><span>{weather?.temperature == null ? "" : "°"}</span></div><div className="condition">{weather?.condition || "Waiting for weather data"}</div><div className="weather-meta">{weather?.feels_like != null ? `Feels like ${weather.feels_like}°` : "Feels like --"}{weather?.high != null && ` · H ${weather.high}°`}{weather?.low != null && ` · L ${weather.low}°`}</div></div><div className="weather-art"><CloudSun size={86} strokeWidth={1.5} /></div></div></article>;
}

function SectionView({ active, data }) {
  const profile = data.user?.profile || {};
  const content = {
    Trends: ["Environmental trends", "See how your environment is changing.", "Your saved assessment trends will appear here when history is available.", data.trends?.length ? data.trends.map(item => item.timestamp || "Assessment") : ["No trend data yet."]],
    Profile: ["Your profile", "Personalize your ClimaCare experience.", "These preferences help the backend tailor future guidance.", [`Age group: ${profile.age_group || "Not set"}`, `Health condition: ${profile.health_condition || "Not set"}`, `Occupation: ${profile.occupation || "Not set"}`]],
    About: ["About ClimaCare AI", "Environmental health guidance, made simple.", "ClimaCare presents local environmental information and backend-provided health guidance.", ["Weather and air-quality insights", "Personalized recommendations", "Environmental information does not replace professional medical advice."]]
  }[active];
  return <section className="section-view"><div className="eyebrow blue-text">{content[0]}</div><h1>{content[1]}</h1><p>{content[2]}</p><div className="section-items">{content[3].map(item => <div className="section-item" key={item}><Check size={18} />{item}</div>)}</div></section>;
}

export default function ClimaCareDashboard() {
  const data = readData();
  const [active, setActive] = useState("Home");
  const [dark, setDark] = useState(false);
  const location = data.location;
  const weather = data.weather;
  const airQuality = data.air_quality;
  return <div className={`app-shell ${dark ? "dark" : ""}`}>
    <AppHeader active={active} setActive={setActive} dark={dark} setDark={setDark} location={location} />
    <main className="page">{active === "Home" ? <>
      <section className="welcome"><div className="eyebrow blue-text">{greeting()}</div><h1>Here’s how today’s environment may affect your health.</h1><p>Simple, personalized environmental health guidance at a glance.</p></section>
      <HeroWeather location={location} weather={weather} />
      <section className="metrics-grid"><MetricCard label="Humidity" value={weather?.humidity} icon={Droplets} unit="%" pending={weather?.humidity == null} /><MetricCard label="AQI" value={airQuality?.aqi} icon={Wind} pending={airQuality?.aqi == null} /><MetricCard label="PM2.5" value={airQuality?.pm25} icon={Activity} unit="µg/m³" pending={airQuality?.pm25 == null} /><MetricCard label="Wind Speed" value={weather?.wind_speed} icon={Navigation} unit="km/h" pending={weather?.wind_speed == null} /></section>
      <section className="main-grid"><RiskCard risk={data.risk} /><AdvisoryCard advisory={data.advisory} risk={data.risk} /><ForecastCard forecast={data.forecast} /></section>
      <section className="bottom-grid"><article className="mini-panel"><div className="mini-title"><ShieldCheck size={20} /> Data Sources</div><p>{data.sources || "Connected sources will be shown here when available."}</p></article><article className="mini-panel"><div className="mini-title"><ShieldCheck size={20} /> Medical Disclaimer</div><p>ClimaCare AI provides environmental health information and does not replace professional medical advice.</p></article></section>
    </> : <SectionView active={active} data={data} />}<footer>ClimaCare AI · Environmental health information for everyday decisions.</footer></main>
    <nav className="mobile-bottom-nav" aria-label="Mobile navigation">{["Home", "Trends", "Profile", "About"].map(link => <button key={link} className={active === link ? "active" : ""} onClick={() => setActive(link)}>{link === "Home" ? <CloudSun size={19} /> : link === "Trends" ? <Activity size={19} /> : link === "Profile" ? <UserRound size={19} /> : <Info size={19} />}<span>{link}</span></button>)}</nav>
  </div>;
}
