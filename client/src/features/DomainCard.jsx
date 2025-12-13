import { Link } from 'react-router';

export default function DomainCard({
  domain,
  status = 'online',
  note = 'in database',
}) {
  return (
    <div className="domain-card">
      <div className="domain-header">
        <span className={`status-dot ${status}`}></span>
        <Link to={`/domains/${domain}`} className="domain-link">
          {domain}
        </Link>
      </div>
      {note && <div className="domain-note">{note}</div>}
    </div>
  );
}
