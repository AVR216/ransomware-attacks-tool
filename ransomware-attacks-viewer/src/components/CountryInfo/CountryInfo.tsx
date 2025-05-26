import { API_BASE_URL } from "../../config";
import { useFetch, useModalContext } from "../../hooks"
import { CountryInfoResponse } from "../../models/models";
import { ErrorDisplay } from "../Error/ErrorDisplay";
import { Loading } from "../Loading/Loading";

export const CountryInfo = () => {

    const { countryCode } = useModalContext();

    const {data, error, loading} = useFetch<CountryInfoResponse>(`${API_BASE_URL}/country/${countryCode}`)

    if (!countryCode) return null;
    if (loading) return <Loading message={`Loading ${countryCode}`} color="dark:bg-gray-800"/>
    if (error) return <ErrorDisplay message={error.message}/>
    if (!data) return null;

    const {
        country,
        total_recent,
        last_attack,
        top_groups,
        top_sectors,
        infostealers,
    } = data.country_info;

    return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 space-y-6 w-full">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{country}</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Recent victims: <span className="font-semibold">{total_recent}</span>
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Last attack: <span className="font-semibold">{last_attack}</span>
        </p>
      </div>

      {/* Top Groups and Sectors */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
            Top Groups
          </h3>
          <div className="flex flex-wrap gap-2">
            {top_groups.map((grp) => (
              <span
                key={grp}
                className="bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 text-sm px-3 py-1 rounded-full"
              >
                {grp}
              </span>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
            Top Sectors
          </h3>
          <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
            {Object.entries(top_sectors).map(([sector, count]) => (
              <li key={sector}>
                <span className="font-medium">{sector}</span>: {count}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Infostealers */}
      { Object.entries(infostealers).length > 0 && 
        <div>
        <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
          Detected Infostealers
        </h3>
        <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
          {Object.entries(infostealers).map(([stealer, count]) => (
            <li key={stealer}>
              <span className="font-medium">{stealer}</span>: {count}
            </li>
          ))}
        </ul>
      </div>
      }
    </div>
  )

}