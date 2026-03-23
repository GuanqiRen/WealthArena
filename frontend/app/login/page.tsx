"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { ApiError } from "@/lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const router = useRouter();

  async function handleSubmit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(email.trim(), password);
      router.replace("/dashboard");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Login failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell" style={{ display: "grid", placeItems: "center" }}>
      <section className="card" style={{ width: "100%", maxWidth: 420, padding: 20 }}>
        <h1 style={{ marginTop: 0 }}>Login</h1>
        <p style={{ color: "var(--muted)" }}>Sign in to view your portfolios and trading history.</p>

        <form className="stack" onSubmit={handleSubmit}>
          <label>
            <div style={{ marginBottom: 6 }}>Email</div>
            <input
              className="input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </label>

          <label>
            <div style={{ marginBottom: 6 }}>Password</div>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </label>

          {error && <p className="error">{error}</p>}

          <button className="btn" type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </section>
    </main>
  );
}
