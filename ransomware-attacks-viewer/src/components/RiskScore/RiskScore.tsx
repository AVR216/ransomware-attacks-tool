import { useState } from "react";
import { LevelOfRiskType, RiskScoreStateObject, TopType } from "../../models";
import { Table } from "../Table/Table";
import { useScoreRisk } from "../../hooks";

export const RiskScore = () => {

    
    const [filters, setFilters] = useState<RiskScoreStateObject>({
        level: 'medium',
        top: 5
    });

    const { data, loading, error } = useScoreRisk(filters);

    const handleLevelChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const value = e.target.value as LevelOfRiskType;
        setFilters(prev => ({ ...prev, level: value }));
    };

    const handleTopChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const value = Number(e.target.value) as TopType;
        setFilters(prev => ({ ...prev, top: value }));
    };

    return (
      <section
      aria-labelledby="risk-groups-title"
      className="h-screen overflow-auto bg-[#1a1a1a] shadow-lg p-6 space-y-6"
        >

        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
        <div>
          <h2
            id="risk-groups-title"
            className="text-2xl font-bold text-gray-900 dark:text-gray-100"
          >
            Risk Groups
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Filter by level and quantity, and see the results in the table below.
          </p>
        </div>

        {/* Filter controls */}
        <div className="flex items-center space-x-4">
          <div>
            <label className="block text-gray-700 dark:text-gray-300 text-sm">
              Level:
            </label>
            <select
              className="mt-1 block w-full bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded p-2"
              value={filters.level}
              onChange={handleLevelChange}
            >
              <option value="">All</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
          <div>
            <label className="block text-gray-700 dark:text-gray-300 text-sm">
              Top:
            </label>
            <select
              className="mt-1 block bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded p-2"
              value={filters.top}
              onChange={handleTopChange}
                >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={15}>15</option>
              <option value={20}>20</option>
            </select>
          </div>
        </div>
      </header>
      <Table data={data} error={error} loading={loading} />
    </section>
    )
}