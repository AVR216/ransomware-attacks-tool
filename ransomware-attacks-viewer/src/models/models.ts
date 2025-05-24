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
    {to: '/by-country', label: 'By Country'}
]