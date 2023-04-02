import axios from "axios";

export const Services = {
  countries: "countries",
  country_codes_table: "country_codes",
  country_data: "country_data",
};

export async function api_request(service) {
  try {
    const response = await axios.get(`http://localhost:5000/${service}`, {
      service,
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

export async function api_request_parameter(service, q) {
  try {
    const response = await axios.get(`http://localhost:5000/${service}/${q}`, {
      service,
      q,
    });
    return response.data;
  } catch (error) {
    console.error(error);
  }
}
