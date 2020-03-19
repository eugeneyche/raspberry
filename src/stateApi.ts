function postToApi<ReturnTy>(route: string, data: {}): Promise<ReturnTy> {
  return fetch(
    `/api/${route}`,
    {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
    }
  )
    .then(resp => {
      const json = resp.json();
      if (!resp.ok) {
        throw json;
      }
      return json;
    })
    .catch(err => err.error);
}

export async function createNamespace(namespace: string): Promise<void> {
  await postToApi('create_namespace', {namespace});
}

export async function listNamespaces(): Promise<Array<string>> {
  return await postToApi('list_namespaces', {});
}

export async function commitState<StateTy>(namespace: string, version: number, data: StateTy): Promise<void> {
  return await postToApi('commit', {namespace, version, data});
}

export async function fetchState<StateTy>(namespace: string, version: number) : Promise<StateTy> {
  return await postToApi('fetch', {namespace, version});
}

export function DEBUG_bindApi() {
  return (window as any).stateApi = {
    createNamespace,
    listNamespaces,
    commitState,
    fetchState,
  };
}