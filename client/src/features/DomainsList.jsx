import React, { useEffect, useState } from "react";
import DomainCard from "./DomainCard";

export default function DomainList() {
  const [domains, setDomains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data from localhost API
  useEffect(() => {
    fetch("http://localhost/api/domains")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch domain list");
        return res.json();
      })
      .then((data) => {
        setDomains(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading domain list...</div>;
  if (error) return <div style={{ color: "red" }}>Error: {error}</div>;

  return (
    <div style={styles.wrapper}>
      {domains.length === 0 ? (
        <h2 style={styles.emptyHeader}>
          No domains available yet
        </h2>
      ) : (
        <div style={styles.listContainer}>
          {domains.map((item) => (
            <DomainCard
              key={item.domain}
              domain={item.domain}
            />
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  wrapper: {
    padding: "20px"
  },
  emptyHeader: {
    textAlign: "center",
    color: "#666",
    fontWeight: "500"
  },
  listContainer: {
    display: "flex",
    gap: "20px",
    flexWrap: "wrap"
  }
};
