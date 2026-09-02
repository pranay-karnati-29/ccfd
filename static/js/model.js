function toggleSidebar() {
  document.querySelector(".sidebar").classList.toggle("open");
}

// Close sidebar when clicking outside
document.addEventListener("click", function (event) {
  const sidebar = document.querySelector(".sidebar");
  const menuToggle = document.querySelector(".menu-toggle");

  if (
    sidebar &&
    menuToggle &&
    !sidebar.contains(event.target) &&
    !menuToggle.contains(event.target)
  ) {
    sidebar.classList.remove("open");
  }
});

// Handle window resize
window.addEventListener("resize", function () {
  const sidebar = document.querySelector(".sidebar");
  if (sidebar && window.innerWidth >= 1200) {
    sidebar.classList.remove("open");
  }
});

document.getElementById("predict-form").onsubmit = async function (e) {
  e.preventDefault();
  const features = document
    .getElementById("features")
    .value.split(",")
    .map(Number);
  const model = document.getElementById("model-select").value;
  const res = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ features, model }),
  });
  const data = await res.json();
  document.getElementById("result").innerHTML = `<b>Prediction:</b> ${
    data.prediction === 1 ? "Fraudulent" : "Legitimate"
  }<br>
                 <b>Probability:</b> ${data.probability.toFixed(4)}<br>
         <b>Accuracy:</b> ${(data.accuracy * 100).toFixed(2)}%`;
};

// Helper functions for sample data
function loadSampleFraud() {
  document.getElementById("features").value =
    "9064,-3.499107537,0.258555161,-4.489558073,4.853894351,-6.974521545,3.628382091,5.431270921,-1.946733711,-0.775680093,-1.987773188,4.690395666,-6.998042432,1.454011986,-3.738023334,0.317742063,-2.013542681,-5.136135103,-1.183822117,1.663394014,-3.042625757,-1.052368256,0.204816874,-2.11900744,0.170278608,-0.393844118,0.296367194,1.985913218,-0.900451638,1809.68";
}

function loadSampleLegit() {
  document.getElementById("features").value =
    "3756,1.350757382,-0.767437703,-0.944464989,-1.595061785,1.432443287,3.284171247,-1.135628638,0.703558091,0.357023709,0.269818306,1.009895195,-3.172259421,1.873844283,1.418459674,0.263151375,1.537059966,0.446842808,-0.860466472,0.758219283,0.275386238,-0.262242226,-0.912080261,0.058162339,0.921364875,0.347414098,-0.511174316,-0.024878235,0.020000189,68.15";
}

function clearFeatures() {
  document.getElementById("features").value = "";
  document.getElementById("result").innerHTML = "";
  document.getElementById("ensemble-result").innerHTML = "";
}

function predictEnsemble() {
  const features = getFeatures();
  const model1 = document.getElementById("model1").value;
  const model2 = document.getElementById("model2").value;

  fetch("/predict_ensemble", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      features: features,
      model1: model1,
      model2: model2,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("ensemble-result").innerHTML = `
                    <h3>Ensemble Results</h3>
                    <div class="result-grid">
                        <div class="result-item">
                            <strong>Ensemble Prediction:</strong> ${
                              data.ensemble_prediction === 1
                                ? "Fraudulent"
                                : "Legitimate"
                            }
                        </div>
                        <div class="result-item">
                            <strong>Average Probability:</strong> ${data.average_probability.toFixed(
                              4
                            )}
                        </div>
                        <div class="result-item">
                            <strong>Max Probability:</strong> ${data.max_probability.toFixed(
                              4
                            )}
                        </div>
                        <div class="result-item">
                            <strong>Model 1 (${model1.toUpperCase()}):</strong> ${
        data.model1.prediction
      } (${data.model1.probability.toFixed(4)})
                        </div>
                        <div class="result-item">
                            <strong>Model 2 (${model2.toUpperCase()}):</strong> ${
        data.model2.prediction
      } (${data.model2.probability.toFixed(4)})
                        </div>
                        <div class="result-item">
                            <strong>Ensemble Accuracy:</strong> ${(
                              data.ensemble_accuracy * 100
                            ).toFixed(2)}%
                        </div>
                    </div>
                `;
    });
}

// Additional ensemble functions
function predictWeighted() {
  const features = getFeatures();
  const model1 = document.getElementById("model1").value;
  const model2 = document.getElementById("model2").value;

  fetch("/predict_weighted", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      features: features,
      model1: model1,
      model2: model2,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("ensemble-result").innerHTML = `
                    <h3>Weighted Ensemble Results</h3>
                    <div class="result-grid">
                        <div class="result-item">
                            <strong>Weighted Prediction:</strong> ${
                              data.weighted_prediction === 1
                                ? "Fraudulent"
                                : "Legitimate"
                            }
                        </div>
                        <div class="result-item">
                            <strong>Weighted Probability:</strong> ${data.weighted_probability.toFixed(
                              4
                            )}
                        </div>
                        <div class="result-item">
                            <strong>Model 1 Weight:</strong> ${data.weights.model1.toFixed(
                              3
                            )}
                        </div>
                        <div class="result-item">
                            <strong>Model 2 Weight:</strong> ${data.weights.model2.toFixed(
                              3
                            )}
                        </div>
                    </div>
                `;
    });
}

function predictSequential() {
  const features = getFeatures();
  const model1 = document.getElementById("model1").value;
  const model2 = document.getElementById("model2").value;

  fetch("/predict_sequential", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      features: features,
      model1: model1,
      model2: model2,
      threshold: 0.7,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("ensemble-result").innerHTML = `
                    <h3>Sequential Prediction Results</h3>
                    <div class="result-grid">
                        <div class="result-item">
                            <strong>Final Prediction:</strong> ${
                              data.final_prediction === 1
                                ? "Fraudulent"
                                : "Legitimate"
                            }
                        </div>
                        <div class="result-item">
                            <strong>Final Probability:</strong> ${data.final_probability.toFixed(
                              4
                            )}
                        </div>
                        <div class="result-item">
                            <strong>Model Used:</strong> ${data.model_used.toUpperCase()}
                        </div>
                        <div class="result-item">
                            <strong>First Model Probability:</strong> ${data.first_model_prob.toFixed(
                              4
                            )}
                        </div>
                    </div>
                `;
    });
}

function getFeatures() {
  const featuresText = document.getElementById("features").value;
  return featuresText.split(",").map(Number);
}
