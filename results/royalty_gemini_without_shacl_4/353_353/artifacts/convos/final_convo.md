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
Prince August Wilhelm Heinrich Günther Viktor of Prussia (29 January 1887 – 25 March 1949), nicknamed "Auwi", was the fourth son of German Emperor Wilhelm II by his first wife, Augusta Victoria of Schleswig-Holstein.
Early life

He was born in the Potsdamer Stadtschloss when his grandfather was still the Crown Prince of Prussia.
He spent his youth with his siblings at the New Palace, also in Potsdam, and his school days with his brothers at the Prinzenhaus in Plön in his mother's ancestral Schleswig-Holstein.
Prince August Wilhelm married his cousin Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg on 22 October 1908 at the Berliner Stadtschloss.
The couple had planned to take up residence in Schönhausen Palace in Berlin, but changed their mind when his father, Kaiser Wilhelm, decided to leave his son the Villa Liegnitz in the Sanssouci Park.
In 1912 their only child, Prince Alexander Ferdinand of Prussia, was born.
In the First World War, August Wilhelm was made district administrator (Landrat) of the district of Ruppin; his office and residence was now Schloss Rheinsberg.
His personal adjutant Hans Georg von Mackensen played an important role in his life; the two had been close friends since August Wilhelm's youth.
These "pronounced homophilic tendencies" contributed to the failure of his marriage to Princess Alexandra Victoria.
The couple did not divorce while August Wilhelm's father, Kaiser Wilhelm II, was Emperor, owing to his opposition to the idea.
Weimar Republic

Initially, many Allied and German leaders favored transitioning Germany to a constitutional monarchy with August Wilhelm as either Emperor or regent for one of Crown Prince Wilhelm's children, although this possibility was quickly precluded when Philipp Scheidemann was forced by the pressures of the German Revolution to declare a republic.
August Wilhelm was awarded custody of their son.
After his divorce and the marriage of his friend von Mackensen to Winifred von Neurath, the daughter of Konstantin von Neurath, August Wilhelm lived a reclusive life in his villa in Potsdam.
Involvement with Nazism

August Wilhelm joined the conservative nationalist veterans group Der Stahlhelm (English: "The Steel helmet").
His involvement with the NSDAP and his adoration of Adolf Hitler made August Wilhelm often the subject of mockery by the left-wing press (who gave him the nickname Braunhemdchen Auwi, or "Auwi the Little Brown Shirt"), politicians (French Ambassador André François-Poncet called him Hanswurst "Hans the Brown Sausage") and from the National Socialists themselves (Joseph Goebbels referred to him as a "good-natured but slightly gormless boy").
As a representative of the erstwhile Hohenzollern dynasty, August Wilhelm was deliberately used by the party to gain votes in elections: he was elected as its lead candidate for the Landtag of Prussia in April 1932, and retained his seat until the Landtag's dissolution in October 1933.
Through his appearances at the party's mass rallies, he addressed himself to sections of the population that were lukewarm towards National Socialism and convinced them "that Hitler was not a threat, but a benefactor of the German people and the German Empire".
At the 5 March 1933 election, August Wilhelm was elected as a Nazi deputy to the German Reichstag from electoral constituency 4, Potsdam I, and he would retain this seat until the fall of the Nazi regime.
August Wilhelm held these positions until the fall of the Nazi regime.
However, after the passing of the Enabling Act of 1933 and the establishment of the dictatorship of the Third Reich, the party no longer needed the former prince, who had secretly hoped "that Hitler would one day hoist him or his son Alexander up to the vacant throne of the Kaiser".
One high-profile visit took August Wilhelm to the Passau Hall of the Nibelungs (Nibelungenhalle).
In early February 1945, in the company of the former Crown Princess Cecilie, August Wilhelm fled the approaching Red Army by going from Potsdam to Kronberg to take refuge with his aunt Princess Margaret of Prussia, a sister of his father.
Post-war life

At the end of the Second World War, on 8 May 1945, August Wilhelm was arrested by the U.S. Army and imprisoned in Ludwigsburg.
A young German Jewish refugee started his interrogation as an American soldier.
Immediately after his release, new proceedings were instituted against August Wilhelm.
With his wife, Princess Alexandra of Schleswig-Holstein-Sonderburg-Glücksburg, Prince August Wilhelm had one son:


Regimental commissions until First World War

Chivalric orders

Ancestry

References

External links



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (2bc292da-16e9-4fe2-a878-fac6509df42b)
 Call ID: 2bc292da-16e9-4fe2-a878-fac6509df42b
  Args:
    type: :Man
    source: August_Wilhelm_of_Prussia
  AssignClass (9292905a-43d0-4cfc-8188-81f0a316f1f8)
 Call ID: 9292905a-43d0-4cfc-8188-81f0a316f1f8
  Args:
    type: :Person
    source: August_Wilhelm_of_Prussia
  AddLiteral (57623026-3bff-47ee-9e54-ec71a980dc1b)
 Call ID: 57623026-3bff-47ee-9e54-ec71a980dc1b
  Args:
    relation: :knownAs
    literal_type: xsd:string
    source: August_Wilhelm_of_Prussia
    literal_value: Auwi
  AddLiteral (13acbf3a-fe07-4ddc-b506-abbd0818454c)
 Call ID: 13acbf3a-fe07-4ddc-b506-abbd0818454c
  Args:
    literal_type: xsd:date
    source: August_Wilhelm_of_Prussia
    literal_value: 1887-01-29
    relation: :hasBirthYear
  AddLiteral (6fa10dac-aae9-4a47-baf2-21abb993ff7e)
 Call ID: 6fa10dac-aae9-4a47-baf2-21abb993ff7e
  Args:
    relation: :hasDeathYear
    source: August_Wilhelm_of_Prussia
    literal_value: 1949-03-25
    literal_type: xsd:date
  AssignClass (58f2d963-f807-4b55-a8a0-95f1bda646d9)
 Call ID: 58f2d963-f807-4b55-a8a0-95f1bda646d9
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (476468f2-5ad6-4755-a2bb-fafd8c5c513d)
 Call ID: 476468f2-5ad6-4755-a2bb-fafd8c5c513d
  Args:
    type: :Person
    source: Wilhelm_II
  AssignClass (9558f863-b47b-4f8f-8214-3e895e8955f4)
 Call ID: 9558f863-b47b-4f8f-8214-3e895e8955f4
  Args:
    type: :Woman
    source: Augusta_Victoria_of_Schleswig-Holstein
  AssignClass (d902f8ab-e8e3-4401-a351-19c192095c96)
 Call ID: d902f8ab-e8e3-4401-a351-19c192095c96
  Args:
    type: :Person
    source: Augusta_Victoria_of_Schleswig-Holstein
  AddTriple (10544bf8-6f62-4bac-97b8-0f0343159920)
 Call ID: 10544bf8-6f62-4bac-97b8-0f0343159920
  Args:
    source: August_Wilhelm_of_Prussia
    relation: :hasFather
    target: Wilhelm_II
  AddTriple (9cad323d-86ba-4522-bf34-850c2184ed90)
 Call ID: 9cad323d-86ba-4522-bf34-850c2184ed90
  Args:
    target: Augusta_Victoria_of_Schleswig-Holstein
    relation: :hasMother
    source: August_Wilhelm_of_Prussia
  AssignClass (216e5c9a-d702-489d-82e6-691054609dda)
 Call ID: 216e5c9a-d702-489d-82e6-691054609dda
  Args:
    type: :Woman
    source: Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AssignClass (1776342c-a952-4919-a12a-b1aa590e8cf3)
 Call ID: 1776342c-a952-4919-a12a-b1aa590e8cf3
  Args:
    source: Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Person
  AddLiteral (87ce30aa-e4ce-4317-8efd-196b31d8f8e3)
 Call ID: 87ce30aa-e4ce-4317-8efd-196b31d8f8e3
  Args:
    relation: :hasMarriageYear
    literal_value: 1908-10-22
    source: August_Wilhelm_of_Prussia
    literal_type: xsd:date
  AddTriple (b5a37c30-15b0-43e5-a59b-d7332c8d9ffe)
 Call ID: b5a37c30-15b0-43e5-a59b-d7332c8d9ffe
  Args:
    target: Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :hasRelation
    source: August_Wilhelm_of_Prussia
  AssignClass (21ab6830-ef8d-4e23-8a7e-c829e2a8dd57)
 Call ID: 21ab6830-ef8d-4e23-8a7e-c829e2a8dd57
  Args:
    source: Alexander_Ferdinand_of_Prussia
    type: :Man
  AssignClass (f1b750c3-3117-47c3-8128-e513665954ce)
 Call ID: f1b750c3-3117-47c3-8128-e513665954ce
  Args:
    source: Alexander_Ferdinand_of_Prussia
    type: :Person
  AddTriple (5fd22b79-adb0-405b-80f7-252fd6a49530)
 Call ID: 5fd22b79-adb0-405b-80f7-252fd6a49530
  Args:
    relation: :isSonOf
    target: August_Wilhelm_of_Prussia
    source: Alexander_Ferdinand_of_Prussia
  AddTriple (5a0e1ae1-de46-41ad-98c7-0deac6a9be17)
 Call ID: 5a0e1ae1-de46-41ad-98c7-0deac6a9be17
  Args:
    source: Alexander_Ferdinand_of_Prussia
    target: Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    relation: :isSonOf
  AssignClass (e28abcc4-e79e-49db-be39-253538ac316c)
 Call ID: e28abcc4-e79e-49db-be39-253538ac316c
  Args:
    type: :Woman
    source: Margaret_of_Prussia
  AssignClass (e886dddb-52e3-4643-8a47-e057a6bb7fcc)
 Call ID: e886dddb-52e3-4643-8a47-e057a6bb7fcc
  Args:
    type: :Person
    source: Margaret_of_Prussia
  AddTriple (d0570086-5dea-4246-9bcb-12772167aa8f)
 Call ID: d0570086-5dea-4246-9bcb-12772167aa8f
  Args:
    relation: :isAuntOf
    target: August_Wilhelm_of_Prussia
    source: Margaret_of_Prussia
  Finish (06fac9b4-2484-4cf4-b771-86f5b9327065)
 Call ID: 06fac9b4-2484-4cf4-b771-86f5b9327065
  Args: