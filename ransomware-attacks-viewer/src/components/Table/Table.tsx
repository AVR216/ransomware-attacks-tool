import { Data, ErrorType, RiskGroupResponse } from "../../models";
import { ErrorDisplay } from "../Error/ErrorDisplay";
import { Loading } from "../Loading/Loading";

interface Props {
    data: Data<RiskGroupResponse[]>;
    loading: boolean;
    error: ErrorType
}

export const Table = ({data, loading, error}: Props) => {

    if (loading) return <Loading message="Loading" />;
    if (error) return <ErrorDisplay message={error.message} />;
    if (!data) return null;

    return (
        <div className="overflow-auto">
      <table className="min-w-full table-auto border-collapse">
        <thead>
          <tr className="bg-gray-200 dark:bg-gray-700">
            <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">Group name</th>
            <th className="px-4 py-2 text-right text-sm font-semibold text-gray-700 dark:text-gray-300">Freq</th>
            <th className="px-4 py-2 text-right text-sm font-semibold text-gray-700 dark:text-gray-300">Countries</th>
            <th className="px-4 py-2 text-right text-sm font-semibold text-gray-700 dark:text-gray-300">Tactics</th>
            <th className="px-4 py-2 text-right text-sm font-semibold text-gray-700 dark:text-gray-300">Score</th>
            <th className="px-4 py-2 text-center text-sm font-semibold text-gray-700 dark:text-gray-300">Level</th>
          </tr>
        </thead>
        <tbody>
          {data.map((g) => (
            <tr key={g.group_name} className="odd:bg-white even:bg-gray-50 dark:odd:bg-gray-800 dark:even:bg-gray-700">
              <td className="px-4 py-2 text-gray-900 dark:text-gray-100">{g.group_name}</td>
              <td className="px-4 py-2 text-right text-gray-900 dark:text-gray-100">{g.freq}</td>
              <td className="px-4 py-2 text-right text-gray-900 dark:text-gray-100">{g.recurrence}</td>
              <td className="px-4 py-2 text-right text-gray-900 dark:text-gray-100">{g.tactics}</td>
              <td className="px-4 py-2 text-right text-gray-900 dark:text-gray-100">{g.risk_score.toFixed(2)}</td>
              <td className="px-4 py-2 text-center">
                <span
                  className={`inline-block px-2 py-1 rounded-full text-xs font-semibold ${
                    g.risk_level === 'high'
                      ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                      : g.risk_level === 'medium'
                      ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
                      : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                  }`}
                >
                  {g.risk_level.charAt(0).toUpperCase() + g.risk_level.slice(1)}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    )
}