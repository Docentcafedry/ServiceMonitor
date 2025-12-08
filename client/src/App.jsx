
import './App.css'
import DomainList from './features/Domains';
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <DomainList/>,
  },
  {
    path: "domain/:domainName",
    element: <><h1>Hello!</h1></>,}
]);

export default function App() {
  return <RouterProvider router={router} />;
}
