import { useState, useEffect } from 'react';
import { useParams } from 'react-router';

function calculateUptime24h(records) {
    const now = new Date();
    const cutoff = new Date(now.getTime() - 24 * 60 * 60 * 1000);

    // 1. Filter only last-24h records
    const last24h = records.filter(item => {
        const t = new Date(item.examination_time);
        return t >= cutoff;
    });

    if (last24h.length === 0) {
        return 0; // no data available
    }

    // 2. Count UP records
    const upCount = last24h.filter(item => item.status_code === 200).length;

    // 3. Calculate percentage
    const uptimePercent = (upCount / last24h.length) * 100;

    return uptimePercent.toFixed(2); // e.g. "98.57"
}

function isoSecondsToMs(isoString) {
    const seconds = parseFloat(isoString.replace("PT", "").replace("S", ""));
    return (seconds * 1000).toFixed(3);
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);

    const pad = n => String(n).padStart(2, "0");

    const hours = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const seconds = pad(date.getSeconds());
    const day = pad(date.getDate());
    const month = pad(date.getMonth() + 1);
    const year = String(date.getFullYear()).slice(2); // last 2 digits

    return `${hours}:${minutes}:${seconds} ${day}-${month}-${year}`;
}


export default function DomainMonitor() {
  const params= useParams()
  const domain = params.domainName
  const [status, setStatus] = useState(null);
  const [responseTime, setResponseTime] = useState(null);
  const [uptime, setUptime] = useState(null);
  const [lastChecked, setLastChecked] = useState(null);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(`http://localhost:8000/examinations/${domain}`);
        const data = await response.json();
        
        if (data) {
          setStatus(data.examinations.at(-1).status_code);
          setResponseTime(isoSecondsToMs(data.examinations.at(-1).response_time));
          setUptime(calculateUptime24h(data.examinations));
          setLastChecked(formatTimestamp(data.examinations.at(-1).examination_time));
          setHistory(data.examinations);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className='page-wrapper'>
      <div className="website-monitor">
      <h2>Мониторинг доступности {domain}</h2>
      <div className="status-info">
        <div>
          <strong>Статус код:</strong> {status || "N/A"}
        </div>
        <div>
          <strong>Время ответа:</strong> {responseTime || "N/A"} ms
        </div>
        <div>
          <strong>Аптайм (24ч):</strong> {uptime || "N/A"}%
        </div>
        <div>
          <strong>Последняя проверка:</strong> {lastChecked || "N/A"}
        </div>
      </div>
      <div className="history">
        <h3>История доступности (последние 24 часа)</h3>
        <div className="history-grid">
          {history.map((item, index) => (
            <div
              key={index}
              className={`history-item ${item.status_code === 200 ? "green" : item.status_code === 500 ? "red" : "gray"}`}
            />
          ))}
        </div>
      </div>
    </div>
    </div>
    
  );
};

