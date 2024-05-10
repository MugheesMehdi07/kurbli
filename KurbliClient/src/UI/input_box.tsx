import { useEffect, useState } from "react";
import { Score } from "../components/score";
import { Checkbox } from "./checkbox";
import { MoonLoader } from "react-spinners";
import { Suggestion } from "../components/suggestions";

const backend_url = `https://1tuwbh5e46.execute-api.ap-southeast-2.amazonaws.com/test`;

export function Input({ toggleScoreBadge, fn, final_score }: any) {
  const [email, setEmail] = useState("");
  const [isEmail, setIsEmail] = useState(true);
  const [user_address, setUser_address] = useState({
    address: "",
    city: "",
    cityAlias: "",
    latitude: 0,
    linkedEntityId: "",
    longitude: 0,
    name: "",
    propertyCount: 1,
    state: "",
    type: "",
    uspsVerified: true,
    zip: "",
    _id: "",
  });
  const [valid_address, setValid_address] = useState(false);
  const [button_text, setButton_text] = useState("NEXT");
  const [score, setScore] = useState(false);
  const [showCheckbox, setShowCheckbox] = useState(true);
  const [isChecked, setIsChecked] = useState(false);
  const [isloading, setIsLoading] = useState(false);
  const [crime_score, setCrime_score] = useState(0);
  const [school_score, setSchool_score] = useState(0);
  const [nsfr_score, setNsfr_score] = useState(0);
  const [rfsr_score, setRfsr_score] = useState(0);
  const [cap_score, setCap_score] = useState(0);

  const [geo_data, setGeo_data] = useState({
    geo_id: "",
    longitude: "",
    latitude: "",
  });


  const handleScoreBadgeClick = () => {
    toggleScoreBadge();
  };

  const fetch_data = async () => {
    try {
      setIsLoading(true);
      const cap_response = await fetch(
        backend_url +
          `/investibility/cap_score?address=${encodeURIComponent(
            user_address.name
          )}`
      );
      const jsonData = await cap_response.json();
      setCap_score(jsonData.cap_score.error ? 0 : jsonData.cap_score);
      const geo_response = await fetch(
        backend_url + `/geo_id?address=${encodeURIComponent(user_address.name)}`
      );
      const geo_json = await geo_response.json();
      setGeo_data(geo_json);
    } catch (error) {
      alert("Cap Score not found");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  setIsEmail(emailRegex.test(email));
}, [email]);

    useEffect(() => {
  if (!geo_data.geo_id) return;

  const fetch_other_data = async () => {
    setIsLoading(true);
    try {
      const urls = [
        `${backend_url}/investibility/crime_score?geo_id=${geo_data.geo_id}`,
        `${backend_url}/investibility/nsfr_score?latitude=${geo_data.latitude}&longitude=${geo_data.longitude}`,
        `${backend_url}/investibility/rfsr_score?latitude=${geo_data.latitude}&longitude=${geo_data.longitude}`,
        `${backend_url}/investibility/school_score?geo_id=${geo_data.geo_id}`
      ];
      const responses = await Promise.all(urls.map(url => fetch(url)));
      const jsonResponses = await Promise.all(responses.map(res => res.json()));

      setCrime_score(jsonResponses[0].crime_score);
      setNsfr_score(jsonResponses[1].n_sfr_score);
      setRfsr_score(jsonResponses[2].r_sfr_score);
      setSchool_score(jsonResponses[3].school_score);
    } catch (error) {
      alert("Error fetching data");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  fetch_other_data();
}, [geo_data.geo_id, backend_url, geo_data.latitude, geo_data.longitude]);

useEffect(() => {
  if (!(nsfr_score && rfsr_score && crime_score && school_score)) return;

  const fetch_kurbil_score = async () => {
    try {
      const url = `${backend_url}/investibility/?address=${encodeURIComponent(user_address.name)}&city=${user_address.city}&state=${user_address.state}&zip=${user_address.zip}&latitude=${geo_data.latitude}&longitude=${geo_data.longitude}&crime_rate=${crime_score}&school_rate=${school_score}&nsfr=${nsfr_score}&rsfr=${rfsr_score}&cap_rate=${cap_score}&email=${email}`;
      const response = await fetch(url);
      const krubil_json = await response.json();
      fn(krubil_json.score);
    } catch (error) {
      console.error("Error fetching the kurbil score", error);
      alert("Error fetching the kurbil score");
    }
  };

  fetch_kurbil_score();
}, [nsfr_score, rfsr_score, crime_score, school_score, backend_url, user_address, geo_data, cap_score, email]);


  const btn_function = () => {
    if (isEmail && isChecked) {
      setButton_text("CALUCULATE SCORE");
      setValid_address(true);
      setShowCheckbox(false);
    }
    if (valid_address && email.length > 0) {
      setScore(true);
      fetch_data();
    }
  };

  return (
    <div className="py-10">
      <div className="flex">
        <div>
          <div className="flex relative">
            {!valid_address && (
              <input
                type={"text"}
                className={`bg-[#FCFAF5] block w-full border ${
                  isEmail ? "border-green-500" : "border-red-500"
                } text-lg rounded-full shadow px-6 font-medium py-3 w-96 pr-12`}
                value={email}
                placeholder={"Enter valid email"}
                required
                onChange={(e) => setEmail(e.target.value)}
              />
            )}
            {valid_address && (
              <div className="bg-[#FCFAF5] block border rounded-full text-lg shadow px-6 font-medium py-3 w-96 pr-12">
                <Suggestion onClick={setUser_address} />
              </div>
            )}
            {isEmail ? (
              <span className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <svg
                  width="250px"
                  height="15px"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    <g id="Warning / Circle_Check">
                      <path
                        id="Vector"
                        d="M15 10L11 14L9 12M12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21Z"
                        stroke="green"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      ></path>
                    </g>
                  </g>
                </svg>
              </span>
            ) : email.length > 0 && !isEmail && !valid_address ? (
              <span className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <svg
                  width="250px"
                  height="15px"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  // style={{ marginTop: "-25px" }}
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    <g id="Warning / Circle_Check">
                      <path
                        d="M12 8H12.01M12 11V16M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                        stroke="red"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      ></path>
                    </g>
                  </g>
                </svg>
              </span>
            ) : null}
            <button
              className="px-6 mx-4 rounded-full bg-[#D9A831] font-bold cursor-pointer relative z-10"
              onClick={btn_function}
            >
              {button_text}
            </button>
          </div>
          {valid_address ||
            (!isEmail && email.trim() != "" && (
              <p className="text-[#FF7575] font-medium px-4">
                Please enter a valid email address
              </p>
            ))}
          {showCheckbox && <Checkbox setIsChecked={setIsChecked} />}
        </div>
      </div>
      {isloading && (
        <div className="flex justify-center mt-4 flex-col items-center">
          <MoonLoader color="#D9A831" size={200} />
          {""}
          <p>Caluculating your kurbli score...</p>
        </div>
      )}
      {score && !isloading && (
        <>
          <div className="flex flex-wrap justify-start mt-4">
            <div
              className="px-1 mb-2 mr-2 bg-[#CFFFEB] flex rounded-full cursor-pointer"
              style={{ whiteSpace: "nowrap" }}
              onClick={handleScoreBadgeClick}
            >
              <img src="/premium.svg" width="20px" height="20px" />
              <div className="px-2 py-2 font-semibold ">
                Kurbli Score: {final_score} |
              </div>
              <svg
                width="25px"
                height="35px"
                viewBox="-0.96 -0.96 25.92 25.92"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g
                  id="SVGRepo_tracerCarrier"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke="#CCCCCC"
                  stroke-width="0.048"
                ></g>
                <g id="SVGRepo_iconCarrier">
                  {" "}
                  <path
                    d="M12 16L12 8"
                    stroke="#323232"
                    stroke-width="1.536"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></path>{" "}
                  <path
                    d="M9 13L11.913 15.913V15.913C11.961 15.961 12.039 15.961 12.087 15.913V15.913L15 13"
                    stroke="#323232"
                    stroke-width="1.536"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></path>{" "}
                  <path
                    d="M3 15L3 16L3 19C3 20.1046 3.89543 21 5 21L19 21C20.1046 21 21 20.1046 21 19L21 16L21 15"
                    stroke="#323232"
                    stroke-width="1.536"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></path>{" "}
                </g>
              </svg>
            </div>

            <Score text={`Crime Score: ${crime_score}`} color="#F5FFCF" />
            <Score text={`School Score: ${school_score}`} color="#CFF1FF" />
            <Score text={`NSFR Score: ${nsfr_score}`} color="#CFD4FF" />
            <Score text={`RFSR Score: ${rfsr_score}`} color="#F8CFFF" />
            <Score text={`CAP Score: ${cap_score}`} color="#FFE6CF" />
          </div>
        </>
      )}
    </div>
  );
}
