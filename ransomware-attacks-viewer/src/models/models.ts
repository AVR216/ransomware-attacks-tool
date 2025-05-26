import { LevelOfRiskType, TopType } from "./Types";

export interface HeatmapItem {
    country: string;
    victims: number;
    lat: number;
    lng: number;
    name: string;
    top_group: string;
}

export interface HeatmapResponse {
    heatmap_info: HeatmapItem[];
}

export interface NavItem {
    to: string;
    label: string;
}

export const navItems: NavItem[] = [
    {to: '/home', label: 'Home'},
    {to: '/heatmap', label: 'Heatmap'},
    {to: 'dangerous-groups', label: 'Dangerous Groups'}
]

export interface CountryInfoResponse {
  country_info: CountryInfo;
}

export interface RiskScoreStateObject {
    level: LevelOfRiskType;
    top: TopType;
}

export interface CountryInfo {
  country: string;
  infostealers: Record<string, number>;
  last_attack: string;
  top_groups: string[];
  top_sectors: Record<string, number>;
  total_recent: number;
}

export interface RiskGroupResponse {
  group_name: string;
  freq: number;
  recurrence: number;
  tactics: number;
  risk_score: number;
  risk_level: LevelOfRiskType;
}
