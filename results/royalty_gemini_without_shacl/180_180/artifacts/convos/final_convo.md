================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Thomas Patrick John Anson, 5th Earl of Lichfield (25 April 1939 – 11 November 2005), was an English photographer from the Anson family.
He inherited the Earldom of Lichfield in 1960 from his paternal grandfather.
In his professional practice he was known as Patrick Lichfield.
Biography

Thomas Patrick John Anson was born on 25 April 1939.
He was the only son of Lieutenant-Colonel Thomas William Arnold Anson, Viscount Anson (1913–1958), the eldest son and heir apparent of Thomas Edward Anson, 4th Earl of Lichfield (1883–1960).
His mother was born Anne Bowes-Lyon (1917–1980), a niece of Queen Elizabeth the Queen Mother.
His parents divorced in 1948, and his mother subsequently became Princess Anne of Denmark after her remarriage to Prince Georg of Denmark in 1950.
He had one sister, Lady Elizabeth Georgiana Anson (1941–2020), who married Sir Geoffrey Adam Shakerley, 6th Baronet.
Lichfield was educated at two boarding independent schools: Wellesley House School in the coastal town of Broadstairs in Kent, and Harrow School in Harrow on the Hill in north-west London, followed by the Royal Military Academy Sandhurst.
His father died in 1958, leaving Patrick to succeed as 5th Earl of Lichfield when his grandfather died in 1960.
Lichfield joined the Grenadier Guards in 1959.
He was selected to take the official photographs of the wedding of the Prince and Princess of Wales in 1981, and subsequently became one of the UK's best-known photographers.
He was chosen by Queen Elizabeth II and the Duke of Edinburgh to take official pictures of her Golden Jubilee in 2002.
He also cameoed in the British sitcom Keeping Up Appearances, appearing in the episode "Sea Fever" as a passenger on the Queen Elizabeth 2.
Lichfield resided in an apartment at the former family seat of Shugborough Hall, near Cannock Chase in Staffordshire.
Marriage and children

On 8 March 1975 Lichfield married Lady Leonora Grosvenor, elder daughter of Robert Grosvenor, 5th Duke of Westminster and Hon.
The Countess of Lichfield has not remarried and has retained her title.
She and the Earl had one son and two daughters together:


Lichfield's most recent partner was the biographer Lady Annunziata Asquith, daughter of Julian Asquith, 2nd Earl of Oxford and Asquith.
Death

On 10 November 2005, Lichfield suffered a major stroke and died the following day at the John Radcliffe Hospital in Oxford.
Lichfield's apartment at Shugborough now houses an exhibition of his work, together with a recreation of his studio.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (3edca207-3096-4cd5-99c7-6fbdbaa7829e)
 Call ID: 3edca207-3096-4cd5-99c7-6fbdbaa7829e
  Args:
    type: :Man
    source: Thomas_Patrick_John_Anson
  AddLiteral (40423bf4-654a-4353-a816-e054f9c84914)
 Call ID: 40423bf4-654a-4353-a816-e054f9c84914
  Args:
    relation: :hasBirthYear
    literal_value: 1939
    literal_type: xsd:integer
    source: Thomas_Patrick_John_Anson
  AddLiteral (d3cc878f-095c-447c-8639-048c6f7f35e8)
 Call ID: d3cc878f-095c-447c-8639-048c6f7f35e8
  Args:
    literal_value: 2005
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Thomas_Patrick_John_Anson
  AddLiteral (a9dc23c7-3948-4850-b653-633f466b30a8)
 Call ID: a9dc23c7-3948-4850-b653-633f466b30a8
  Args:
    literal_type: xsd:string
    source: Thomas_Patrick_John_Anson
    literal_value: Patrick Lichfield
    relation: :knownAs
  AssignClass (34bbfec8-8170-4f03-80f7-cc3b1e97d8c7)
 Call ID: 34bbfec8-8170-4f03-80f7-cc3b1e97d8c7
  Args:
    source: Thomas_William_Arnold_Anson
    type: :Man
  AddLiteral (45ed697b-dad6-44a1-894e-26965f70e188)
 Call ID: 45ed697b-dad6-44a1-894e-26965f70e188
  Args:
    relation: :hasBirthYear
    literal_value: 1913
    literal_type: xsd:integer
    source: Thomas_William_Arnold_Anson
  AddLiteral (a73ea4a9-7435-42d3-b800-a237de0756ec)
 Call ID: a73ea4a9-7435-42d3-b800-a237de0756ec
  Args:
    source: Thomas_William_Arnold_Anson
    literal_type: xsd:integer
    literal_value: 1958
    relation: :hasDeathYear
  AddTriple (a7f47dea-3a10-4aff-8beb-c86df98cbaec)
 Call ID: a7f47dea-3a10-4aff-8beb-c86df98cbaec
  Args:
    target: Thomas_Patrick_John_Anson
    relation: :isFatherOf
    source: Thomas_William_Arnold_Anson
  AssignClass (535d4e5d-e238-47d1-a5d3-5f234a6f61c0)
 Call ID: 535d4e5d-e238-47d1-a5d3-5f234a6f61c0
  Args:
    type: :Man
    source: Thomas_Edward_Anson
  AddLiteral (f85b8196-3f04-4053-9b18-a7c5c1530a57)
 Call ID: f85b8196-3f04-4053-9b18-a7c5c1530a57
  Args:
    literal_value: 1883
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Thomas_Edward_Anson
  AddLiteral (36984243-5399-4b45-b7bc-1e2f65c67f8a)
 Call ID: 36984243-5399-4b45-b7bc-1e2f65c67f8a
  Args:
    literal_type: xsd:integer
    source: Thomas_Edward_Anson
    literal_value: 1960
    relation: :hasDeathYear
  AddTriple (1a2fba09-7932-4613-b85f-4c4b388b8d77)
 Call ID: 1a2fba09-7932-4613-b85f-4c4b388b8d77
  Args:
    source: Thomas_Edward_Anson
    target: Thomas_William_Arnold_Anson
    relation: :isFatherOf
  AssignClass (28245494-1020-4160-9992-3ea022ca1b59)
 Call ID: 28245494-1020-4160-9992-3ea022ca1b59
  Args:
    source: Anne_Bowes-Lyon
    type: :Woman
  AddLiteral (ce661219-55b4-4661-92fd-d35b0fa00db7)
 Call ID: ce661219-55b4-4661-92fd-d35b0fa00db7
  Args:
    literal_type: xsd:integer
    source: Anne_Bowes-Lyon
    relation: :hasBirthYear
    literal_value: 1917
  AddLiteral (6ccc183d-c5e5-4978-940a-0c08b115cecc)
 Call ID: 6ccc183d-c5e5-4978-940a-0c08b115cecc
  Args:
    source: Anne_Bowes-Lyon
    literal_type: xsd:integer
    literal_value: 1980
    relation: :hasDeathYear
  AddTriple (00f31795-0bd4-4f06-ae06-8c67b7e53fe8)
 Call ID: 00f31795-0bd4-4f06-ae06-8c67b7e53fe8
  Args:
    source: Anne_Bowes-Lyon
    relation: :isMotherOf
    target: Thomas_Patrick_John_Anson
  AssignClass (5ac6ae83-a85f-4589-a5d4-ae3e3b10216f)
 Call ID: 5ac6ae83-a85f-4589-a5d4-ae3e3b10216f
  Args:
    type: :Woman
    source: Elizabeth_Georgiana_Anson
  AddLiteral (8fe4cb03-cc64-4d80-9af3-26e030d07c4c)
 Call ID: 8fe4cb03-cc64-4d80-9af3-26e030d07c4c
  Args:
    relation: :hasBirthYear
    literal_value: 1941
    source: Elizabeth_Georgiana_Anson
    literal_type: xsd:integer
  AddLiteral (25103400-2133-4414-8084-2f6a9773a3d0)
 Call ID: 25103400-2133-4414-8084-2f6a9773a3d0
  Args:
    literal_type: xsd:integer
    source: Elizabeth_Georgiana_Anson
    relation: :hasDeathYear
    literal_value: 2020
  AddTriple (5d73d2df-2f99-41e4-8f72-051b0de3f925)
 Call ID: 5d73d2df-2f99-41e4-8f72-051b0de3f925
  Args:
    relation: :isSisterOf
    target: Thomas_Patrick_John_Anson
    source: Elizabeth_Georgiana_Anson
  AssignClass (31550938-55af-4bf9-90c0-8764e1ec1e86)
 Call ID: 31550938-55af-4bf9-90c0-8764e1ec1e86
  Args:
    type: :Woman
    source: Leonora_Grosvenor
  AddTriple (c92cfcee-33cb-4aed-bf74-7edacad644f4)
 Call ID: c92cfcee-33cb-4aed-bf74-7edacad644f4
  Args:
    source: Thomas_Patrick_John_Anson
    target: Leonora_Grosvenor
    relation: :hasRelation
  AddLiteral (090cc801-8981-4aa0-8df2-f4498043c061)
 Call ID: 090cc801-8981-4aa0-8df2-f4498043c061
  Args:
    source: Thomas_Patrick_John_Anson
    literal_type: xsd:integer
    literal_value: 1975
    relation: :hasMarriageYear
  AssignClass (10077c57-a372-4fbe-91bd-c3adff0a6340)
 Call ID: 10077c57-a372-4fbe-91bd-c3adff0a6340
  Args:
    type: :Man
    source: Robert_Grosvenor
  AddTriple (80677174-fd25-404f-aeae-e0c9196af800)
 Call ID: 80677174-fd25-404f-aeae-e0c9196af800
  Args:
    source: Robert_Grosvenor
    relation: :isFatherOf
    target: Leonora_Grosvenor
  AssignClass (76294c29-8e5c-4e7d-b805-c26687050f6c)
 Call ID: 76294c29-8e5c-4e7d-b805-c26687050f6c
  Args:
    source: Annunziata_Asquith
    type: :Woman
  AddTriple (ea4dff83-2666-4507-b0c0-0447f04e89f3)
 Call ID: ea4dff83-2666-4507-b0c0-0447f04e89f3
  Args:
    source: Thomas_Patrick_John_Anson
    target: Annunziata_Asquith
    relation: :hasRelation
  AssignClass (92db30f4-42b9-44f7-8672-a172e14dcc81)
 Call ID: 92db30f4-42b9-44f7-8672-a172e14dcc81
  Args:
    type: :Man
    source: Julian_Asquith
  AddTriple (a61648c8-d401-435a-99e0-b86118a1a5e4)
 Call ID: a61648c8-d401-435a-99e0-b86118a1a5e4
  Args:
    target: Annunziata_Asquith
    relation: :isFatherOf
    source: Julian_Asquith
  Finish (06b88b48-afc5-452d-9684-3cca18138d2b)
 Call ID: 06b88b48-afc5-452d-9684-3cca18138d2b
  Args: