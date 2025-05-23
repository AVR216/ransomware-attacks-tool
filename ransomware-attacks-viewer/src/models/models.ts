export interface HeatmapItem {
    country: string;
    victims: number;
    latlng?: [number, number];
    countryName?: string;
}

export interface HeatmapResponse {
    heatmap_info: HeatmapItem[];
}