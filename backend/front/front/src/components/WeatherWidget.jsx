// src/components/WeatherWidget.jsx
import { useEffect, useState } from "react";
import { getWeather } from "../services/weatherService";

export default function WeatherWidget({ city = "Seoul" }) {
  const [data, setData] = useState([]); // ✅ 배열
  const [theme, setTheme] = useState("clear");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    async function fetchWeather() {
      try {
        const forecast = await getWeather(city);
        console.log("✅ Weather data:", forecast);

        if (!active || !forecast) return;
        setData(forecast);

        // 오늘 날씨 기준으로 테마 설정
        const today = forecast[0];
        const code = (today.main || "").toLowerCase();
        if (code.includes("clear")) setTheme("clear");
        else if (code.includes("night") || code.includes("cloud")) setTheme("night");
        else setTheme("sand");
      } catch (err) {
        console.error("❌ WeatherWidget Error:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchWeather();
    return () => { active = false };
  }, [city]);

  if (loading) {
    return (
      <div className="rounded-xl text-text-soft p-7 min-h-[120px] bg-bg-widget backdrop-blur">
        ☁️ 날씨 불러오는 중...
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="rounded-xl text-text-soft p-7 min-h-[120px] bg-bg-widget backdrop-blur">
        ❌ 표시할 날씨 정보가 없습니다.
      </div>
    );
  }

  // ✅ 테마 스타일 정의
  const themeBg = {
    clear: "bg-gradient-weather-clear",
    night: "bg-gradient-weather-night",
    sand: "bg-gradient-weather-sand",
  }[theme] || "bg-gradient-weather";

  const today = data[0];

  return (
    <div
      className={`rounded-xl text-text p-7 min-h-[252px] flex flex-col gap-4.5 ${themeBg} relative overflow-hidden`}
    >
      <div className="absolute inset-0 bg-[linear-gradient(135deg,rgba(255,255,255,0.12),rgba(255,255,255,0.04))] pointer-events-none"></div>

      {/* ✅ 오늘 날씨 요약 */}
      <div className="relative z-10">
        <h3 className="m-0 mb-2.5 font-bold text-lg leading-snug">
          📍 {city} ({today.date})
        </h3>
        <div className="text-[44px] font-extrabold leading-tight">
          {Math.round(today.temp)}°
        </div>
        <p className="mt-0.5 text-sm leading-relaxed">
          {today.main} · {today.desc}
        </p>
      </div>

      {/* ✅ 날씨 세부 요소 (간단 요약) */}
      <div className="flex gap-3 relative z-10 flex-wrap">
        <div className="bg-white/25 px-2.5 py-1.5 rounded-xl text-xs font-semibold backdrop-blur">
          💧 강수확률 {Math.round(today.rainProb)}%
        </div>
        <div className="bg-white/25 px-2.5 py-1.5 rounded-xl text-xs font-semibold backdrop-blur">
          🌡️ 체감온도 {Math.round(today.temp)}°C
        </div>
      </div>

      {/* ✅ 5일 예보 미니카드 */}
      <div className="grid grid-cols-5 gap-2.5 relative z-10 mt-2">
        {data.map((day, i) => (
          <div
            key={i}
            className="bg-emerald-50/90 px-2.5 py-2 text-center rounded-xl backdrop-blur"
          >
            <div className="text-xs opacity-90">
              {day.date.split("-").slice(1).join("/")}
            </div>
            <div>{day.main === "Clear" ? "☀️" : "☁️"}</div>
            <div className="font-bold mt-0.5 text-sm">
              {Math.round(day.temp)}°
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}



// import { useEffect, useState } from 'react'
// import { getWeather } from '../services/weatherService'

// // 현재 날씨를 조회/표시, API 키 없으면 '목업' 데이터로 대체
// export default function WeatherWidget({city='Seoul'}){
//   const [data,setData] = useState(null)
//   const [theme,setTheme] = useState('clear')

//   useEffect(()=>{
//     let on = true
//     getWeather(city).then(w=>{
//       if(!on) return
//       setData(w)
//       const code = (w.main||'').toLowerCase()
//       if(code.includes('clear')) setTheme('clear')
//       else if(code.includes('night')|| code.includes('cloud')) setTheme('night')
//       else setTheme('sand')
//     })
//     return ()=>{ on=false }
//   },[city])

//   if(!data){
//     return <div className="rounded-xl text-text-soft p-7 min-h-[120px] bg-bg-widget backdrop-blur">날씨 불러오는 중...</div>
//   }

//   const themeBg = {
//     clear: 'bg-gradient-weather-clear',
//     night: 'bg-gradient-weather-night',
//     sand: 'bg-gradient-weather-sand',
//   }[theme] || 'bg-gradient-weather'

//   return (
//     <div className={`rounded-xl text-text p-7 min-h-[252px] flex flex-col gap-4.5 ${themeBg} relative overflow-hidden`}>
//       <div className="absolute inset-0 bg-[linear-gradient(135deg,rgba(255,255,255,0.12),rgba(255,255,255,0.04))] pointer-events-none"></div>
//       <div className="relative z-10">
//         <div>
//           <h3 className="m-0 mb-2.5 font-bold text-lg leading-snug">{data.city}</h3>
//           <div className="text-[44px] font-extrabold leading-tight">{Math.round(data.temp)}°</div>
//           <p className="mt-0.5 text-sm leading-relaxed">{data.main} · {data.desc}</p>
//         </div>
//       </div>
//       <div className="flex gap-3 relative z-10 flex-wrap">
//         <div className="bg-white/25 px-2.5 py-1.5 rounded-xl text-xs font-semibold backdrop-blur">💧 {data.humidity}%</div>
//         <div className="bg-white/25 px-2.5 py-1.5 rounded-xl text-xs font-semibold backdrop-blur">🌬️ {data.wind} m/s</div>
//         <div className="bg-white/25 px-2.5 py-1.5 rounded-xl text-xs font-semibold backdrop-blur">☁️ {data.clouds}%</div>
//       </div>
//       <div className="grid grid-cols-6 gap-2.5 relative z-10">
//         {data.hourly.slice(0,6).map((h,i)=> (
//           <div key={i} className="bg-emerald-50/90 px-2.5 py-2 text-center rounded-xl backdrop-blur">
//             <div className="text-xs opacity-90">{h.t}</div>
//             <div>{h.i}</div>
//             <div className="font-bold mt-0.5 text-sm">{Math.round(h.temp)}°</div>
//           </div>
//         ))}
//       </div>
//     </div>
//   )
// }
