"use client";

type GoogleSignInButtonProps = {
  onClick: () => void;
  disabled?: boolean;
};

export default function GoogleSignInButton({
  onClick,
  disabled = false,
}: GoogleSignInButtonProps) {
  return (
    <button
      type="button"
      className="btn btn-google"
      onClick={onClick}
      disabled={disabled}
      aria-label="Continue with Google"
    >
      <span aria-hidden="true">G</span>
      <span>{disabled ? "Redirecting to Google..." : "Continue with Google"}</span>
    </button>
  );
}
