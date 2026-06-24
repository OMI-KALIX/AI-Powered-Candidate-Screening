from graph.graph import graph
import pandas as pd

final_state = graph.invoke({})

results = pd.DataFrame(

    final_state["results"]

)


results.to_csv(

    "candidate_results.csv",

    index=False

)

print("Results Saved Successfully.")