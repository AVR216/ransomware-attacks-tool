interface Props {
  message: string;
  color?: string;
}

export const Loading = ({message, color = 'bg-[#1a1a1a]'}: Props) => {
  return (
    <div className={`flex items-center justify-center h-full w-full ${color}`}>
        <div className="flex flex-col items-center space-y-2">
        {/* Spinner */}
        <svg
            className="animate-spin h-10 w-10 text-[#00FF00]"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
        >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
        />
      </svg>
      {/* Text */}
      <span className="text-[#00FF00] text-lg font-semibold">
        {message}
      </span>
    </div>
  </div>
  )
}