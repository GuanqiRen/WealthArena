import type { Session } from "@supabase/supabase-js";
import { getSupabaseClient } from "@/lib/supabase";

export async function signInWithGoogle(): Promise<void> {
  const supabase = getSupabaseClient();
  if (!supabase) {
    throw new Error("Supabase is not configured for Google sign-in.");
  }

  const redirectTo =
    typeof window === "undefined" ? undefined : `${window.location.origin}/dashboard`;

  const { error } = await supabase.auth.signInWithOAuth({
    provider: "google",
    options: { redirectTo },
  });

  if (error) {
    throw error;
  }
}

export async function getSupabaseAccessToken(): Promise<string | null> {
  const supabase = getSupabaseClient();
  if (!supabase) {
    return null;
  }

  const { data, error } = await supabase.auth.getSession();
  if (error) {
    return null;
  }

  return data.session?.access_token ?? null;
}

export function subscribeToSupabaseAuthChanges(
  onChange: (session: Session | null) => void,
): (() => void) | null {
  const supabase = getSupabaseClient();
  if (!supabase) {
    return null;
  }

  const { data } = supabase.auth.onAuthStateChange((_event, session) => {
    onChange(session);
  });

  return () => {
    data.subscription.unsubscribe();
  };
}

export async function signOutSupabase(): Promise<void> {
  const supabase = getSupabaseClient();
  if (!supabase) {
    return;
  }

  await supabase.auth.signOut();
}
