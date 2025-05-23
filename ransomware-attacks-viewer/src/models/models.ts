export interface HeatmapItem {
    country: string;
    victims: number;
    lat: number;
    lng: number;
    name: string;
}

export interface HeatmapResponse {
    heatmap_info: HeatmapItem[];
}