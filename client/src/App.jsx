
import './App.css'
import DomainList from './features/Domains';
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";
import DomainMonitor from './features/DomainMonitor';

const router = createBrowserRouter([
  {
    path: "/",
    element: <DomainList/>,
  },
  {
    path: "domains/:domainName",
    element: <DomainMonitor></DomainMonitor>,}
]);

export default function App() {
  return <RouterProvider router={router} />;
}
