import { NavLink } from "react-router-dom";
import { NavItem } from "../../models/models";

interface SidebarProps {
    items: NavItem[];
}

export const Sidebar = ({items}: SidebarProps) => {
    return(
         <aside className="w-64 bg-black text-gray-100 h-screen shadow-lg flex flex-col">
            <div className="p-6 border-b border-gray-700">
            <h2 className="text-2xl text-[#00FF00] font-bold">RansomScan Tool</h2>
            </div>

            <nav className="flex-1 overflow-y-auto">
            <ul className="mt-4 space-y-1">
                {items.map(({ to, label }) => (
                <li key={to}>
                    <NavLink
                    to={to}
                    end={to === '/'}
                    className={({ isActive }) =>
                        `flex items-center py-2 px-4 transition-colors rounded-lg mx-2 ${
                        isActive
                            ? 'bg-gray-700 text-white'
                            : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                        }`
                    }
                    >
                    <span className="ml-2">{label}</span>
                    </NavLink>
                </li>
                ))}
            </ul>
            </nav>
        </aside>
    )
}