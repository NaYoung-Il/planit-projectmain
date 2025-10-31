// src/components/WeatherAlertModal.jsx
import { useEffect, useState } from "react";
import { getTripWeatherMessages } from "../services/weatherService";

export default function WeatherAlertModal({ trip, onClose }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadWeather() {
      try {
        setLoading(true);
        const result = await getTripWeatherMessages(trip);
        console.log("🌦 여행 알림 데이터:", result);
        setMessages(result);
      } catch (e) {
        console.error("❌ 날씨 불러오기 실패:", e);
      } finally {
        setLoading(false);
      }
    }
    loadWeather();
  }, [trip]);

  if (!trip) return null;

  const now = new Date();
  const dDay = Math.ceil(
    (new Date(trip.start_date) - now) / (1000 * 60 * 60 * 24)
  );

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-400 hover:text-gray-600 text-lg"
        >
          ✖
        </button>

        <h2 className="text-xl font-bold text-emerald-700 mb-2">
          ✈️ {trip.city_name} 여행 D-{dDay}
        </h2>
        <p className="text-sm text-gray-600 mb-4">
          ({trip.start_date} ~ {trip.end_date})
        </p>

        {loading ? (
          <p className="text-gray-500 text-sm">🌥 날씨 정보를 불러오는 중...</p>
        ) : messages.length > 0 ? (
          <div className="space-y-2">
            {messages.map((m, i) => (
              <div
                key={i}
                className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-sm"
              >
                <strong className="text-emerald-700">
                  {m.summary || `Day ${m.day}`}:
                </strong>{" "}
                {m.advice}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">
            ❌ 표시할 날씨 알림이 없습니다.
          </p>
        )}
      </div>
    </div>
  );
}
