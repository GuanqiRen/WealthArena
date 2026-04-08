import { createClient, type SupabaseClient } from "@supabase/supabase-js";

let supabaseClient: SupabaseClient | null = null;

function getSupabaseConfig(): { url: string; publicKey: string } | null {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const publicKey =
    process.env.NEXT_PUBLIC_SUPABASE_PUBLIC_KEY ??
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!url || !publicKey) {
    return null;
  }

  return { url, publicKey };
}

export function isSupabaseConfigured(): boolean {
  return getSupabaseConfig() !== null;
}

export function getSupabaseClient(): SupabaseClient | null {
  const config = getSupabaseConfig();
  if (!config) {
    return null;
  }

  if (!supabaseClient) {
    supabaseClient = createClient(config.url, config.publicKey, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
        detectSessionInUrl: true,
      },
    });
  }

  return supabaseClient;
}
