const BASE_URL = "http://localhost:5000/api";


/** given data about a cupcake, generate html */

function generateCupcakeHTML(cupcake) {
  return `
    <div data-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-btn">X</button>
      </li>
      <img class="Cupcake-img"
            src="${cupcake.image}">
    </div>
  `;
}


/** queries the API to get the cupcakes and adds to the page */

async function showInitialCupcakes() {
  const resp = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcake of resp.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcake));

    $("#cupcakes-list").append(newCupcake);
  }
}


/** handle form for adding of new cupcakes */

$("#cupcake-add-form").on("submit", async function (evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  const resp = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  let newCupcake = $(generateCupcakeHTML(resp.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#cupcake-add-form").trigger("reset");
});


/** handle button delete cupcake */

$("#cupcakes-list").on("click", ".delete-btn", async function (evt) {
  evt.preventDefault();

  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();

});


$(showInitialCupcakes);