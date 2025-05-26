interface Props {
  message: string;
}

export const ErrorDisplay = ({ message }: Props) => {
  return (
    <div className="flex items-center justify-center h-full w-full bg-[#1a1a1a]">
      <div className="flex flex-col items-center space-y-2">
        {/* Icono de error */}
        <svg
          className="h-10 w-10 text-red-500"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 9v2m0 4h.01M21 12A9 9 0 103 12a9 9 0 0018 0z"
          />
        </svg>
        {/* Texto */}
        <span className="text-red-400 text-lg font-semibold text-center px-4">
          {message}
        </span>
      </div>
    </div>
  );
};
