import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const analyzeText = async () => {
    if (!text.trim()) {
      setError("Please enter some text to analyze");
      return;
    }
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("http://localhost:8000/analyze-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        throw new Error(`Backend error: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Backend not reachable. Make sure uvicorn is running on http://localhost:8000");
      console.error(err);
    }

    setLoading(false);
  };

  const analyzeFile = async (endpoint) => {
    if (!file) {
      setError("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`http://localhost:8000/${endpoint}`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Backend error: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Backend not reachable. Make sure uvicorn is running on http://localhost:8000");
      console.error(err);
    }

    setLoading(false);
  };

  const trustScore = result?.final_score ?? 0;
  const confidence = result?.confidence ?? "Unknown";
  const factScore = result?.fact_score ?? 0;
  const sourceScore = result?.source_score ?? 0;
  const sentimentScore = result?.sentiment_score ?? 0;

  // Normalize sentiment from -1 to 1 range to 0 to 1 range for display
  const sentimentNormalized = (sentimentScore + 1) / 2;

  // Determine verdict color based on final score
  const verdictColor =
    trustScore >= 0.7
      ? "#4ade80"
      : trustScore >= 0.4
      ? "#facc15"
      : "#ef4444";

  // Determine verdict text based on score
  const getVerdict = () => {
    if (trustScore >= 0.7) return "TRUSTWORTHY";
    if (trustScore >= 0.4) return "INCONCLUSIVE";
    return "UNRELIABLE";
  };

  const chartData = result
    ? [
        { name: "Fact", value: Math.min(1, Math.max(0, factScore)) },
        { name: "Source", value: Math.min(1, Math.max(0, sourceScore)) },
        { name: "Sentiment", value: Math.min(1, Math.max(0, sentimentNormalized)) },
      ]
    : [];

  return (
    <div
      style={{
        width: "100vw",
        minHeight: "100vh",
        background: "linear-gradient(135deg, #0a1428 0%, #0f2845 50%, #1a3a52 100%)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
        fontFamily: "'Segoe UI', 'Inter', sans-serif",
        color: "white",
        margin: 0,
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "1400px",
          boxSizing: "border-box",
        }}
      >
        {/* HEADER */}
        <div
          style={{
            textAlign: "center",
            marginBottom: "50px",
          }}
        >
          <h1
            style={{
              fontSize: "42px",
              fontWeight: "700",
              marginBottom: "8px",
              background: "linear-gradient(135deg, #00d4ff, #00ffff)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
              letterSpacing: "-0.5px",
            }}
          >
            TruthLens
          </h1>
          <p
            style={{
              fontSize: "16px",
              color: "#a0aec0",
              fontWeight: "400",
              letterSpacing: "0.5px",
            }}
          >
            Trust Score Dashboard
          </p>
        </div>

        {/* ERROR MESSAGE */}
        {error && (
          <div
            style={{
              background: "rgba(239, 68, 68, 0.1)",
              border: "1px solid rgba(239, 68, 68, 0.5)",
              borderRadius: "10px",
              padding: "16px",
              marginBottom: "30px",
              color: "#fca5a5",
              fontSize: "14px",
              display: "flex",
              alignItems: "center",
              gap: "12px",
            }}
          >
            <span style={{ fontSize: "18px" }}>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* MAIN CONTAINER */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "40px",
            marginTop: "30px",
          }}
        >
          {/* LEFT CARD - ANALYSIS */}
          <div
            style={{
              background: "linear-gradient(135deg, rgba(15, 40, 69, 0.8) 0%, rgba(20, 55, 80, 0.6) 100%)",
              padding: "40px",
              borderRadius: "20px",
              boxShadow: "0 20px 60px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
              border: "1px solid rgba(0, 200, 255, 0.2)",
              backdropFilter: "blur(10px)",
            }}
          >
            {/* TEXT ANALYSIS SECTION */}
            <div style={{ marginBottom: "35px" }}>
              <h3
                style={{
                  fontSize: "18px",
                  fontWeight: "600",
                  marginBottom: "15px",
                  color: "#00d4ff",
                  textTransform: "uppercase",
                  letterSpacing: "1px",
                }}
              >
                📝 Analyze Text
              </h3>

              <textarea
                rows="6"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter a claim or statement to verify. Example: 'The Earth orbits the Sun in...'"
                style={{
                  width: "100%",
                  padding: "14px 16px",
                  borderRadius: "12px",
                  border: "1px solid rgba(0, 200, 255, 0.3)",
                  background: "rgba(10, 25, 45, 0.8)",
                  color: "white",
                  fontFamily: "inherit",
                  fontSize: "14px",
                  lineHeight: "1.6",
                  resize: "vertical",
                  transition: "all 0.3s ease",
                  outline: "none",
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = "rgba(0, 200, 255, 0.8)";
                  e.target.style.boxShadow = "0 0 20px rgba(0, 212, 255, 0.2)";
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = "rgba(0, 200, 255, 0.3)";
                  e.target.style.boxShadow = "none";
                }}
              />
              <div style={{ fontSize: "12px", color: "#64748b", marginTop: "8px", textAlign: "right" }}>
                {text.length} characters
              </div>

              <button
                onClick={analyzeText}
                disabled={loading}
                style={{
                  marginTop: "16px",
                  width: "100%",
                  padding: "14px 24px",
                  borderRadius: "10px",
                  border: "none",
                  background: loading 
                    ? "linear-gradient(135deg, #666666 0%, #555555 100%)" 
                    : "linear-gradient(135deg, #00b4d8 0%, #00d4ff 100%)",
                  color: loading ? "#999" : "#0a1428",
                  fontWeight: "600",
                  fontSize: "15px",
                  cursor: loading ? "not-allowed" : "pointer",
                  transition: "all 0.3s ease",
                  boxShadow: loading 
                    ? "0 4px 12px rgba(0, 0, 0, 0.2)" 
                    : "0 8px 20px rgba(0, 180, 216, 0.3)",
                  textTransform: "uppercase",
                  letterSpacing: "0.5px",
                  opacity: loading ? 0.7 : 1,
                }}
                onMouseEnter={(e) => {
                  if (!loading) {
                    e.target.style.transform = "translateY(-2px)";
                    e.target.style.boxShadow = "0 12px 30px rgba(0, 180, 216, 0.5)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (!loading) {
                    e.target.style.transform = "translateY(0)";
                    e.target.style.boxShadow = "0 8px 20px rgba(0, 180, 216, 0.3)";
                  }
                }}
              >
                {loading ? "⏳ Analyzing..." : "✓ Analyze Text"}
              </button>
            </div>

            {/* DIVIDER */}
            <div
              style={{
                height: "1px",
                background: "linear-gradient(90deg, rgba(0, 200, 255, 0), rgba(0, 200, 255, 0.3), rgba(0, 200, 255, 0))",
                margin: "35px 0",
              }}
            />

            {/* FILE ANALYSIS SECTION */}
            <div>
              <h3
                style={{
                  fontSize: "18px",
                  fontWeight: "600",
                  marginBottom: "15px",
                  color: "#00d4ff",
                  textTransform: "uppercase",
                  letterSpacing: "1px",
                }}
              >
                🎬 Media Analysis
              </h3>

              <label
                style={{
                  display: "block",
                  marginBottom: "16px",
                  cursor: "pointer",
                }}
              >
                <input
                  type="file"
                  onChange={(e) => {
                    setFile(e.target.files[0]);
                    setError(null);
                  }}
                  accept="image/*,video/*"
                  style={{
                    opacity: "0",
                    position: "absolute",
                    width: "0",
                    height: "0",
                  }}
                />
                <div
                  style={{
                    padding: "20px",
                    borderRadius: "12px",
                    border: "2px dashed rgba(0, 200, 255, 0.4)",
                    background: "rgba(0, 212, 255, 0.05)",
                    textAlign: "center",
                    transition: "all 0.3s ease",
                    color: "#a0aec0",
                    fontSize: "14px",
                  }}
                  onMouseEnter={(e) => {
                    e.style.borderColor = "rgba(0, 200, 255, 0.8)";
                    e.style.background = "rgba(0, 212, 255, 0.15)";
                    e.style.color = "#00d4ff";
                  }}
                  onMouseLeave={(e) => {
                    e.style.borderColor = "rgba(0, 200, 255, 0.4)";
                    e.style.background = "rgba(0, 212, 255, 0.05)";
                    e.style.color = "#a0aec0";
                  }}
                >
                  {file ? (
                    <div>
                      <div style={{ fontSize: "20px", marginBottom: "6px" }}>✅</div>
                      <div style={{ fontWeight: "600", marginBottom: "4px" }}>{file.name}</div>
                      <div style={{ fontSize: "12px", color: "#64748b" }}>
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </div>
                    </div>
                  ) : (
                    <div>
                      <div style={{ fontSize: "20px", marginBottom: "6px" }}>📂</div>
                      Click to select or drag & drop image/video here
                    </div>
                  )}
                </div>
              </label>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "12px",
                }}
              >
                <button
                  onClick={() => analyzeFile("analyze-image")}
                  disabled={!file || loading}
                  style={{
                    padding: "12px 20px",
                    borderRadius: "10px",
                    border: "none",
                    background: !file || loading
                      ? "linear-gradient(135deg, #666666 0%, #555555 100%)"
                      : "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
                    color: !file || loading ? "#999" : "white",
                    cursor: !file || loading ? "not-allowed" : "pointer",
                    fontWeight: "600",
                    fontSize: "14px",
                    transition: "all 0.3s ease",
                    boxShadow: !file || loading
                      ? "0 4px 12px rgba(0, 0, 0, 0.2)"
                      : "0 6px 20px rgba(59, 130, 246, 0.3)",
                    textTransform: "uppercase",
                    letterSpacing: "0.5px",
                    opacity: !file || loading ? 0.6 : 1,
                  }}
                  onMouseEnter={(e) => {
                    if (file && !loading) {
                      e.target.style.transform = "translateY(-2px)";
                      e.target.style.boxShadow = "0 10px 30px rgba(59, 130, 246, 0.5)";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (file && !loading) {
                      e.target.style.transform = "translateY(0)";
                      e.target.style.boxShadow = "0 6px 20px rgba(59, 130, 246, 0.3)";
                    }
                  }}
                >
                  {loading ? "⏳" : "🖼️"} Image
                </button>

                <button
                  onClick={() => analyzeFile("analyze-video")}
                  disabled={!file || loading}
                  style={{
                    padding: "12px 20px",
                    borderRadius: "10px",
                    border: "none",
                    background: !file || loading
                      ? "linear-gradient(135deg, #666666 0%, #555555 100%)"
                      : "linear-gradient(135deg, #a855f7 0%, #9333ea 100%)",
                    color: !file || loading ? "#999" : "white",
                    cursor: !file || loading ? "not-allowed" : "pointer",
                    fontWeight: "600",
                    fontSize: "14px",
                    transition: "all 0.3s ease",
                    boxShadow: !file || loading
                      ? "0 4px 12px rgba(0, 0, 0, 0.2)"
                      : "0 6px 20px rgba(168, 85, 247, 0.3)",
                    textTransform: "uppercase",
                    letterSpacing: "0.5px",
                    opacity: !file || loading ? 0.6 : 1,
                  }}
                  onMouseEnter={(e) => {
                    if (file && !loading) {
                      e.target.style.transform = "translateY(-2px)";
                      e.target.style.boxShadow = "0 10px 30px rgba(168, 85, 247, 0.5)";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (file && !loading) {
                      e.target.style.transform = "translateY(0)";
                      e.target.style.boxShadow = "0 6px 20px rgba(168, 85, 247, 0.3)";
                    }
                  }}
                >
                  {loading ? "⏳" : "🎥"} Video
                </button>
              </div>
            </div>
          </div>

          {/* RIGHT CARD - RESULTS */}
          <div
            style={{
              background: "linear-gradient(135deg, rgba(15, 40, 69, 0.8) 0%, rgba(20, 55, 80, 0.6) 100%)",
              padding: "40px",
              borderRadius: "20px",
              boxShadow: "0 20px 60px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
              border: "1px solid rgba(0, 200, 255, 0.2)",
              backdropFilter: "blur(10px)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
            }}
          >
            <h3
              style={{
                fontSize: "18px",
                fontWeight: "600",
                marginBottom: "30px",
                color: "#00d4ff",
                textTransform: "uppercase",
                letterSpacing: "1px",
                textAlign: "center",
              }}
            >
              📊 Trust Score
            </h3>

            <div style={{ textAlign: "center" }}>
              {/* SCORE DISPLAY */}
              <div
                style={{
                  marginBottom: "30px",
                }}
              >
                <h2
                  style={{
                    fontSize: "64px",
                    fontWeight: "700",
                    color: verdictColor,
                    marginBottom: "15px",
                    textShadow: `0 0 30px ${verdictColor}80`,
                  }}
                >
                  {(trustScore).toFixed(3)}
                </h2>

                {/* PROGRESS BAR */}
                <div
                  style={{
                    height: "12px",
                    background: "rgba(50, 70, 100, 0.6)",
                    borderRadius: "10px",
                    overflow: "hidden",
                    marginBottom: "20px",
                    boxShadow: "inset 0 2px 4px rgba(0, 0, 0, 0.3)",
                  }}
                >
                  <div
                    style={{
                      width: `${Math.max(0, Math.min(100, trustScore * 100))}%`,
                      height: "100%",
                      background: `linear-gradient(90deg, ${verdictColor}, ${verdictColor}dd)`,
                      borderRadius: "10px",
                      transition: "width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)",
                      boxShadow: `0 0 20px ${verdictColor}60`,
                    }}
                  />
                </div>
              </div>

              {result && (
                <>
                  {/* VERDICT BADGE */}
                  <div
                    style={{
                      display: "inline-block",
                      padding: "12px 28px",
                      borderRadius: "25px",
                      background: verdictColor,
                      color: "#0a1428",
                      fontSize: "14px",
                      fontWeight: "700",
                      textTransform: "uppercase",
                      letterSpacing: "0.5px",
                      marginBottom: "20px",
                      boxShadow: `0 8px 20px ${verdictColor}50`,
                    }}
                  >
                    {getVerdict()}
                  </div>

                  {/* CONFIDENCE */}
                  <p
                    style={{
                      fontSize: "14px",
                      color: "#a0aec0",
                      marginBottom: "20px",
                      letterSpacing: "0.3px",
                    }}
                  >
                    Confidence: <span style={{ color: verdictColor, fontWeight: "600" }}>{confidence}</span>
                  </p>

                  {/* DETAILED SCORES */}
                  <div
                    style={{
                      background: "rgba(0, 212, 255, 0.05)",
                      padding: "16px",
                      borderRadius: "10px",
                      marginBottom: "20px",
                      border: "1px solid rgba(0, 200, 255, 0.2)",
                    }}
                  >
                    <h5
                      style={{
                        fontSize: "12px",
                        color: "#a0aec0",
                        textTransform: "uppercase",
                        letterSpacing: "1px",
                        marginBottom: "12px",
                      }}
                    >
                      Component Scores
                    </h5>
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns: "1fr",
                        gap: "10px",
                        fontSize: "13px",
                      }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span style={{ color: "#cbd5e1" }}>📋 Fact Check:</span>
                        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                          <div style={{ width: "100px", height: "6px", background: "rgba(0, 200, 255, 0.2)", borderRadius: "3px" }}>
                            <div style={{ width: `${Math.min(100, factScore * 100)}%`, height: "100%", background: "#4ade80", borderRadius: "3px" }} />
                          </div>
                          <span style={{ color: "#4ade80", fontWeight: "600", minWidth: "40px" }}>{(factScore).toFixed(3)}</span>
                        </div>
                      </div>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span style={{ color: "#cbd5e1" }}>🔗 Source:</span>
                        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                          <div style={{ width: "100px", height: "6px", background: "rgba(0, 200, 255, 0.2)", borderRadius: "3px" }}>
                            <div style={{ width: `${Math.min(100, sourceScore * 100)}%`, height: "100%", background: "#3b82f6", borderRadius: "3px" }} />
                          </div>
                          <span style={{ color: "#3b82f6", fontWeight: "600", minWidth: "40px" }}>{(sourceScore).toFixed(3)}</span>
                        </div>
                      </div>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span style={{ color: "#cbd5e1" }}>😊 Sentiment:</span>
                        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                          <div style={{ width: "100px", height: "6px", background: "rgba(0, 200, 255, 0.2)", borderRadius: "3px" }}>
                            <div style={{ width: `${Math.min(100, sentimentNormalized * 100)}%`, height: "100%", background: "#a855f7", borderRadius: "3px" }} />
                          </div>
                          <span style={{ color: "#a855f7", fontWeight: "600", minWidth: "40px" }}>{(sentimentNormalized).toFixed(3)}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* BREAKDOWN TITLE */}
                  <h4
                    style={{
                      fontSize: "14px",
                      fontWeight: "600",
                      color: "#00d4ff",
                      textTransform: "uppercase",
                      letterSpacing: "1px",
                      marginBottom: "20px",
                    }}
                  >
                    📊 Score Breakdown
                  </h4>

                  {/* CHART */}
                  <ResponsiveContainer width="100%" height={240}>
                    <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 200, 255, 0.1)" vertical={false} />
                      <XAxis dataKey="name" stroke="#a0aec0" style={{ fontSize: "12px" }} />
                      <YAxis domain={[0, 1]} stroke="#a0aec0" style={{ fontSize: "12px" }} />
                      <Tooltip
                        contentStyle={{
                          background: "rgba(10, 20, 40, 0.95)",
                          border: "1px solid rgba(0, 200, 255, 0.5)",
                          borderRadius: "8px",
                          padding: "12px",
                        }}
                        labelStyle={{ color: "#fff" }}
                        formatter={(value) => [(value).toFixed(3), "Score"]}
                      />
                      <Bar dataKey="value" fill="#00d4ff" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </>
              )}

              {!result && (
                <div
                  style={{
                    padding: "60px 20px",
                    textAlign: "center",
                    color: "#64748b",
                  }}
                >
                  <p style={{ fontSize: "18px", marginBottom: "8px" }}>👈 Analyze Text or Media</p>
                  <p style={{ fontSize: "13px" }}>Results and scores will appear here</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* RESPONSIVE - STACK ON MOBILE */}
        <style>{`
          @media (max-width: 1024px) {
            div[style*="gridTemplateColumns"] {
              grid-template-columns: 1fr !important;
            }
          }
        `}</style>
      </div>
    </div>
  );
}

export default App;