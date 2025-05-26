import { API_BASE_URL } from "../config";
import { RiskGroupResponse, RiskScoreStateObject } from "../models";
import { useFetch } from "./useFetch";

export const useScoreRisk = ({ level, top = 5 }: RiskScoreStateObject) => {
    let url = `${API_BASE_URL}/risk/groups?top=${top}`;
    if (level) url += `&level=${level}`;

    const { data, error, loading } = useFetch<RiskGroupResponse[]>(url);

    return { data, error, loading };
}