import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="CRM Accounting Sync",layout="wide")
st.title("CRM ↔ Accounting Sync Platform")
st.caption("Synthetic event-driven synchronization, duplicate controls, conflict handling, and finance reconciliation.")
random.seed(21)
statuses=["Synced","Synced","Synced","Retry","Conflict","Duplicate Blocked"]
rows=[]
for i in range(140):
    deal=round(random.uniform(2500,85000),2)
    status=random.choice(statuses)
    rows.append({"deal_id":f"D-{1000+i}","customer":f"Customer {random.randint(1,70):03}","deal_value":deal,"crm_stage":random.choice(["Closed Won","Closed Won","Contracted"]),"invoice_value":deal if status not in ["Conflict"] else round(deal*random.uniform(.92,1.08),2),"sync_status":status,"event":random.choice(["deal.closed","customer.updated","payment.received"]),"attempts":1 if status=="Synced" else random.randint(2,5)})
df=pd.DataFrame(rows)
df["variance"]=df.invoice_value-df.deal_value

status_filter=st.sidebar.multiselect("Sync status",sorted(df.sync_status.unique()),default=sorted(df.sync_status.unique()))
f=df[df.sync_status.isin(status_filter)]

c1,c2,c3,c4=st.columns(4)
c1.metric("Events",len(f))
c2.metric("Synced",int((f.sync_status=="Synced").sum()))
c3.metric("Exceptions",int((f.sync_status!="Synced").sum()))
c4.metric("Value monitored",f"${f.deal_value.sum()/1e6:,.1f}M")

st.subheader("Sync health")
summary=f.groupby("sync_status",as_index=False).agg(events=("deal_id","count"),value=("deal_value","sum"))
st.plotly_chart(px.bar(summary,x="sync_status",y="events",hover_data=["value"]),use_container_width=True)

left,right=st.columns(2)
with left:
    st.subheader("Event volume")
    evt=f.groupby("event",as_index=False).size()
    st.plotly_chart(px.pie(evt,names="event",values="size"),use_container_width=True)
with right:
    st.subheader("Commercial vs accounting values")
    st.plotly_chart(px.scatter(f,x="deal_value",y="invoice_value",color="sync_status",hover_name="deal_id"),use_container_width=True)

st.subheader("Exception queue")
exc=f[f.sync_status!="Synced"].copy().sort_values("attempts",ascending=False)
st.dataframe(exc[["deal_id","customer","event","deal_value","invoice_value","variance","sync_status","attempts"]],use_container_width=True,hide_index=True)

st.subheader("Control flow")
st.code("""CRM webhook received
→ validate event idempotency
→ normalize customer + deal payload
→ look up accounting customer/invoice
→ create or update only when rules pass
→ block duplicates/conflicts
→ retry transient failures
→ write immutable audit event
→ surface unresolved exceptions to human review""")
