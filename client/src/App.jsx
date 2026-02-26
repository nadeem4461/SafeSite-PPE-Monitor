import { useEffect,useState } from "react";

function App(){
  const [incidents , setIncidents] = useState([]);
  useEffect(()=>{
    fetch('http://127.0.0.1:8000/api/incidents')
    .then(res=>res.json())
    .then(data=>setIncidents(data))
    .catch(err=>console.error("Error fetching data :",err));
  },[]);
  
  return(
    <div style={{ padding: '40px', fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <h1 style={{ borderBottom: '3px solid #007bff', paddingBottom: '10px' }}>🚧 SafeSite PPE Monitor Dashboard</h1>
      
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f1f3f5', borderBottom: '2px solid #dee2e6' }}>
              <th style={{ padding: '12px' }}>Incident ID</th>
              <th style={{ padding: '12px' }}>Timestamp</th>
              <th style={{ padding: '12px' }}>Violation Type</th>
              <th style={{ padding: '12px' }}>Evidence Snapshot</th>
            </tr>

          </thead>

          <tbody>
            {incidents.map(incident => (
              <tr key={incident.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                <td style={{ padding: '12px', fontWeight: 'bold' }}>#{incident.id}</td>
                <td style={{ padding: '12px' }}>{incident.timestamp}</td>
                <td style={{ padding: '12px', color: '#dc3545', fontWeight: 'bold' }}>{incident.violation_type}</td>
                <td style={{ padding: '12px' }}>
                  <img 
                    src={`http://127.0.0.1:8000/${incident.image_path}`} 
                    alt="Violation Evidence" 
                    style={{ height: '100px', borderRadius: '4px', border: '1px solid #ccc' }}
                  />
                </td>
              </tr>
            ))}
          </tbody>
          </table>
          </div>
          </div>
  );
}
export default App;
