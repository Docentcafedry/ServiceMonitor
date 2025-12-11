
import './App.css'
import DomainList from './features/Domains';
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";
import DomainMonitor from './features/DomainMonitor';
import AddDomainForm from './features/AddDomainForm';

const router = createBrowserRouter([
  {
    path: "/",
    element: <DomainList/>,
  },
  {
    path: "domains/:domainName",
    element: <DomainMonitor></DomainMonitor>,
  },
  {
    path: "domains/add",
    element: <AddDomainForm></AddDomainForm>,
  },


]);

export default function App() {
  return <RouterProvider router={router} />;
}
