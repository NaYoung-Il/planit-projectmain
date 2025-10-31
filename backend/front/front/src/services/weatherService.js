import axios from "axios";

const key = import.meta.env.VITE_OPEN_WEATHER_KEY;
const BASE_URL = "https://api.openweathermap.org/data/2.5";

console.log("🔑 VITE_OPEN_WEATHER_KEY:", import.meta.env.VITE_OPEN_WEATHER_KEY);


// ✅ 기존: 도시명 기반 실시간 예보 (3시간 단위)
export async function getWeather(city) {
  if (!key) return null;
  try {
    const res = await axios.get(`${BASE_URL}/forecast`, {
      params: { q: city, appid: key, units: "metric", lang: "kr" },
    });
    const data = res.data;

    // 날짜별 정오(12시) 데이터만 추출
    const dailyForecast = {};
    data.list.forEach((item) => {
      const [date, time] = item.dt_txt.split(" ");
      if (time.startsWith("12:")) {
        dailyForecast[date] = {
          date,
          temp: item.main.temp,
          rainProb: item.pop * 100,
          main: item.weather?.[0]?.main || "",
          desc: item.weather?.[0]?.description || "",
        };
      }
    });

    return Object.values(dailyForecast);
  } catch (err) {
    console.warn("Weather API fail, using mock", err.message);
    return null;
  }
}

// ✅ 기존: lat/lon 기반 조회
export async function getForecast(lat, lon) {
  if (!key) return null;
  const res = await axios.get(`${BASE_URL}/forecast`, {
    params: { lat, lon, appid: key, units: "metric", lang: "kr" },
  });
  return res.data;
}

// ✅ 기존: 조건별 멘트
export function createWeatherMessage({ date, temp, rainProb, main }) {
  let msg = "";
  const d = new Date(date);
  const day = `${d.getMonth() + 1}/${d.getDate()}`;


  if (rainProb > 60) msg = `☔ ${day} 비 예보 — 우산을 챙기세요!`;
  else if (temp < 17) msg = `🧥 ${day} 기온 ${Math.round(temp)}° — 겉옷을 챙기세요!`;
  else if (temp > 28) msg = `🕶 ${day} 맑고 더움 — 선글라스 추천!`;
  else msg = `🌤 ${day} ${main} — 날씨가 좋아요!`;

  return msg;
}

// ✅ [새로 추가] 여행 일정 기반 맞춤형 멘트
export async function getTripWeatherMessages(trip) {
  const { city_name, lat, lon, start_date, end_date, diffDays } = trip;

  console.log('📅 trip 기간:', start_date, end_date);
  console.log('📡 lat/lon:', lat, lon);

  // 1️⃣ 위도/경도 기반 예보
  const forecastData = await getForecast(lat, lon);
  if (!forecastData || !forecastData.list) {
    console.warn("❌ 예보 데이터가 없습니다.");
    return [];
  }

  // 2️⃣ 날짜별 정오(12시) 데이터만 추출
  const daily = {};
  forecastData.list.forEach((item) => {
    const [date, time] = item.dt_txt.split(" ");
    if (time.startsWith("12:")) {
      daily[date] = {
        date,
        temp: item.main.temp,
        rainProb: item.pop * 100,
        main: item.weather?.[0]?.main || "",
      };
    }
  });

  // 3️⃣ 여행 기간 필터링
  const allDays = Object.values(daily);
  const start = new Date(start_date);
  const end = new Date(end_date);
  const tripDays = allDays.filter((d) => {
    const date = new Date(d.date);
    return date >= start && date <= end;
  });

  // 4️⃣ 남은 일수(D-4~D-1)에 맞게 표시할 날짜 제한
  const showDays = Math.min(5 - diffDays + 1, tripDays.length);

  // 5️⃣ 날짜별 메시지 생성
  const messages = tripDays.slice(0, showDays).map((d) => createWeatherMessage(d));

  // 6️⃣ 여행 이름 / 도시명 포함해서 표시
  const withCityMessages = messages.map(
    (msg, i) => `📅 ${city_name} ${tripDays[i]?.date} — ${msg}`
  );

  console.log("🌦️ 생성된 여행 메시지:", withCityMessages);
  return withCityMessages; // ✅ 문자열 배열 리턴!
}

// ✅ 기존: 목업
function mockWeather(city) {
  return Promise.resolve({
    city,
    main: "Clear",
    desc: "맑음(목업)",
    temp: 23,
    humidity: 55,
    wind: 2,
    clouds: 12,
    hourly: [
      { t: "12:00", i: "☀️", temp: 24 },
      { t: "14:00", i: "⛅", temp: 25 },
      { t: "16:00", i: "☀️", temp: 26 },
      { t: "18:00", i: "🌤️", temp: 24 },
      { t: "20:00", i: "🌙", temp: 22 },
      { t: "22:00", i: "🌙", temp: 21 },
    ],
  });
}

// import axios from 'axios'

// const key = import.meta.env.VITE_OPEN_WEATHER_KEY

// // 도시명으로 실시간 날씨 정보 조회 (API 키 없으면 목업 데이터 반환)
// export async function getWeather(city){
//   if(!key){
//     return null
//   }
//   try{
//     const res = await axios.get('https://api.openweathermap.org/data/2.5/forecast',{
//       params: { q: city, appid: key, units: 'metric', lang: 'kr'},
//     })
//     const data = res.data

//     // 날짜별 활동량이 가장 많은 시간(정오 12시) 데이터 만 추출
//     const dailyForecast = {}
//     data.list.forEach((item) =>{
//       const [date, time] = item.dt_txt.split(' ')
//       if (time.startsWith('12:')) {
//         dailyForecast[date]={
//           date,
//           temp: item.main.temp,
//           rainProb: item.pop * 100,
//           main: item.weather?.[0]?.main || '',
//           desc: item.weather?.[0]?.description || '',
//         }
//       }
//     })

//     return Object.values(dailyForecast)
//   }catch(err){
//     console.warn('Weather API fail, using mock', err.message)
//     return null
//   }
// }

// //lat/lon 경도 위도 기반 검색
// export async function getForecast(lat, lon) {
//   const res = await axios.get(
//     `${BASE_URL}/forecast?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=kr`
//   )
//   return res.data
// }

// // 날씨 조건에 따른 멘트
// export function createWeatherMessge({ date, temp, rainProb, main}){
//   let msg = ''
//   const d = new Date(date)
//   const day = `${d.getMonth() + 1}/${d.getDate()}`

//   if (rainProb > 60) msg = `☔ ${day} 비 예보 — 우산을 챙기세요!`
//   else if (temp < 17) msg = `🧥 ${day} 기온 ${Math.round(temp)}° — 겉옷을 챙기세요!`
//   else if (temp > 28) msg = `🕶 ${day} 맑고 더움 — 썬글라스 추천!`  
//   else msg = `🌤 ${day} ${main} — 날씨가 좋아요!`
  
//   return msg
// }

// //여행 일정 기준 멘트
// export async function getTripWeatherMessages(city, startDate, endDate, diffDays) {
//   const forecast = await getWeatherForecast(city)
//   if (!forecast) return []
  
  
//   const messages = []
//   const tripDays = []
  
  
//   let start = new Date(startDate)
//   let end = new Date(endDate)
  
  
//   // 🔸 여행 일수 계산 (최대 5일까지만)
//   const totalDays = Math.min(
//   1 + Math.floor((end - start) / (1000 * 60 * 60 * 24)),
//   5
//   )
  
  
//   // 🔸 남은 일수(diffDays)에 따라 몇 일치 예보를 보여줄지 결정
//   const showDays = Math.min(5 - diffDays + 1, totalDays)
  
  
//   for (let i = 0; i < showDays; i++) {
//   const target = new Date(start)
//   target.setDate(start.getDate() + i)
//   const key = target.toISOString().split('T')[0]
  
  
//   const dayData = forecast.find((f) => f.date === key)
//   if (dayData) {
//   messages.push(createWeatherMessage(dayData))
//   }
//   }
  

//   return messages
//   }

// // 목업 날씨 데이터 반환
// function mockWeather(city){
//   return Promise.resolve({
//     city,
//     main: 'Clear',
//     desc: '맑음(목업)',
//     temp: 23,
//     humidity: 55,
//     wind: 2,
//     clouds: 12,
//     hourly: [
//       {t:'12:00', i:'☀️', temp:24},
//       {t:'14:00', i:'⛅', temp:25},
//       {t:'16:00', i:'☀️', temp:26},
//       {t:'18:00', i:'🌤️', temp:24},
//       {t:'20:00', i:'🌙', temp:22},
//       {t:'22:00', i:'🌙', temp:21}
//     ]
//   })
// }

