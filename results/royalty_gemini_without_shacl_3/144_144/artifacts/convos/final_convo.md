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
Prince Christoph of Hesse (Christoph Ernst August; 14
May 1901 – 7 October 1943) was a nephew of Kaiser Wilhelm II.
His brother-in-law Prince Philip of Greece and Denmark fought on the British side and married the future Queen Elizabeth II after the war.
Birth

Prince Christoph of Hesse was born in Frankfurt, the fifth son of Prince Frederick Charles of Hesse and Princess Margaret of Prussia.
He was a twin, with Prince Richard of Hesse.
His father, Frederick Charles, a scion of the House of Hesse, was elected King of Finland in 1918, when Finland declared its independence after the collapse of the Russian Empire.
Christoph's mother was the daughter of Emperor Frederick III and of Victoria, Princess Royal.
Prince Christoph was thus a great-grandson of Queen Victoria and Prince Albert of Saxe-Coburg and Gotha.
Christoph had several brothers, including Prince Philipp and Prince Wolfgang.
His two eldest brothers, Friedrich Wilhelm and Maximilian, both died in World War I.


Career and death

Prince Christoph was a director in the Third Reich's Ministry of Air Forces, Commander of the Air Reserves, and held the rank of Oberführer in the SS.
His brother Prince Philipp joined Hitler's SA.
They were not the only family members to embrace Nazism; their mother "Mossy" (a sister of Kaiser Wilhelm II) invited Adolf Hitler to tea and flew the swastika from her home at Schloss Kronberg.
According to the historian Hugo Vickers, Prince Christoph became "disenchanted" with the Nazi Party by the time of the assassination of Reinhard Heydrich in 1942.
"


Prince Christoph served in the Luftwaffe Research Office and, in 1942, he joined the staff of a fighter unit, Jagdgeschwader 53.
After the Allied Invasion of Italy, Christoph was recalled to Germany, but was killed during his return.
His body and the body of his copilot Wilhelm Gsteu were found two days later and were buried in a German military cemetery near Forlì.
Family

Christoph married his second cousin, once removed, Princess Sophie of Greece and Denmark on 15 December 1930 in Kronberg im Taunus, Germany.
Princess Sophie was the youngest daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, and the sister of the future Prince Philip, Duke of Edinburgh.
The couple had five children:


Some years after Christoph's death, his widow married Prince George William of Hanover, a brother of Queen Fredrica of Greece and a grandson of Kaiser Wilhelm II.
Four years after Christoph's death, his widow's brother, Philip, married the future Queen Elizabeth II.
Christoph's surviving children are first cousins of King Charles III.



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
  AssignClass (724cf795-28ad-461f-b13a-87424d3a6790)
 Call ID: 724cf795-28ad-461f-b13a-87424d3a6790
  Args:
    source: Prince_Christoph_of_Hesse
    type: :Man
  AddLiteral (cae9f253-a824-4c65-a2e5-978a3e88c0f3)
 Call ID: cae9f253-a824-4c65-a2e5-978a3e88c0f3
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Christoph_of_Hesse
    literal_value: 1901
  AddLiteral (e18da1ef-9f2d-46af-bda7-2886878d66e2)
 Call ID: e18da1ef-9f2d-46af-bda7-2886878d66e2
  Args:
    source: Prince_Christoph_of_Hesse
    literal_value: 1943
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (58170f9c-9775-4c50-a179-cb9fdfd9b829)
 Call ID: 58170f9c-9775-4c50-a179-cb9fdfd9b829
  Args:
    type: :Man
    source: Prince_Frederick_Charles_of_Hesse
  AssignClass (6690bdb1-c127-4ae4-8168-ec5c5dfc222f)
 Call ID: 6690bdb1-c127-4ae4-8168-ec5c5dfc222f
  Args:
    type: :Woman
    source: Princess_Margaret_of_Prussia
  AddTriple (69e9dcad-3b12-4741-bf35-17a067c761fc)
 Call ID: 69e9dcad-3b12-4741-bf35-17a067c761fc
  Args:
    relation: :hasFather
    source: Prince_Christoph_of_Hesse
    target: Prince_Frederick_Charles_of_Hesse
  AddTriple (ea5a0d30-46fb-4407-ac67-62df1984200c)
 Call ID: ea5a0d30-46fb-4407-ac67-62df1984200c
  Args:
    source: Prince_Christoph_of_Hesse
    target: Princess_Margaret_of_Prussia
    relation: :hasMother
  AssignClass (270d713d-722a-4658-a302-f83bbf9de840)
 Call ID: 270d713d-722a-4658-a302-f83bbf9de840
  Args:
    source: Prince_Richard_of_Hesse
    type: :Man
  AddTriple (e46bb1e9-8846-4dbb-913d-fb15660a6888)
 Call ID: e46bb1e9-8846-4dbb-913d-fb15660a6888
  Args:
    relation: :isSiblingOf
    target: Prince_Richard_of_Hesse
    source: Prince_Christoph_of_Hesse
  AssignClass (f9ecbdd9-e5fc-4e0a-8b4f-7d1e69abbc94)
 Call ID: f9ecbdd9-e5fc-4e0a-8b4f-7d1e69abbc94
  Args:
    source: Emperor_Frederick_III
    type: :Man
  AssignClass (f0bf0d8b-50c6-4e73-9bf1-907e7e4b6c73)
 Call ID: f0bf0d8b-50c6-4e73-9bf1-907e7e4b6c73
  Args:
    source: Victoria_Princess_Royal
    type: :Woman
  AddTriple (d4b8845b-5888-484b-ba84-4e7ea0a8e3c9)
 Call ID: d4b8845b-5888-484b-ba84-4e7ea0a8e3c9
  Args:
    source: Princess_Margaret_of_Prussia
    target: Emperor_Frederick_III
    relation: :hasFather
  AddTriple (942d2cad-3bda-4684-9fbb-520cffa0b706)
 Call ID: 942d2cad-3bda-4684-9fbb-520cffa0b706
  Args:
    source: Princess_Margaret_of_Prussia
    target: Victoria_Princess_Royal
    relation: :hasMother
  AssignClass (95e6e487-ff9a-4c45-959d-60dc665e274b)
 Call ID: 95e6e487-ff9a-4c45-959d-60dc665e274b
  Args:
    type: :Man
    source: Prince_Philipp_of_Hesse
  AssignClass (8f0e3072-a71f-4067-9b38-474035095467)
 Call ID: 8f0e3072-a71f-4067-9b38-474035095467
  Args:
    source: Prince_Wolfgang_of_Hesse
    type: :Man
  AssignClass (e9445a79-2e2c-4b16-b8f9-41493d86c625)
 Call ID: e9445a79-2e2c-4b16-b8f9-41493d86c625
  Args:
    type: :Man
    source: Friedrich_Wilhelm_of_Hesse
  AssignClass (f3be608c-f229-4c67-a3ef-ade338983452)
 Call ID: f3be608c-f229-4c67-a3ef-ade338983452
  Args:
    type: :Man
    source: Maximilian_of_Hesse
  AddTriple (2f56ca4a-e626-43ae-a045-fd5935d21d27)
 Call ID: 2f56ca4a-e626-43ae-a045-fd5935d21d27
  Args:
    target: Prince_Philipp_of_Hesse
    source: Prince_Christoph_of_Hesse
    relation: :isSiblingOf
  AddTriple (5dce2a11-7983-4f32-a4bd-66af0e365817)
 Call ID: 5dce2a11-7983-4f32-a4bd-66af0e365817
  Args:
    target: Prince_Wolfgang_of_Hesse
    source: Prince_Christoph_of_Hesse
    relation: :isSiblingOf
  AddTriple (8e8f2ab2-d9eb-41e8-8d97-bd8822880167)
 Call ID: 8e8f2ab2-d9eb-41e8-8d97-bd8822880167
  Args:
    relation: :isSiblingOf
    source: Prince_Christoph_of_Hesse
    target: Friedrich_Wilhelm_of_Hesse
  AddTriple (37e09106-853a-4bb6-97f1-e5a4ca0236a5)
 Call ID: 37e09106-853a-4bb6-97f1-e5a4ca0236a5
  Args:
    relation: :isSiblingOf
    source: Prince_Christoph_of_Hesse
    target: Maximilian_of_Hesse
  AssignClass (329ac06e-78f5-4938-aafc-19a6d4df9ecb)
 Call ID: 329ac06e-78f5-4938-aafc-19a6d4df9ecb
  Args:
    source: Princess_Sophie_of_Greece_and_Denmark
    type: :Woman
  AddLiteral (64c57c27-a1e1-44b2-a291-04771cb6c2bd)
 Call ID: 64c57c27-a1e1-44b2-a291-04771cb6c2bd
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1930
    source: Prince_Christoph_of_Hesse
  AddTriple (d18a24af-ba34-4541-856c-980fb10ab761)
 Call ID: d18a24af-ba34-4541-856c-980fb10ab761
  Args:
    relation: :hasRelation
    source: Prince_Christoph_of_Hesse
    target: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (9c32fb60-f4da-41f2-9a1b-3a0dd413fedc)
 Call ID: 9c32fb60-f4da-41f2-9a1b-3a0dd413fedc
  Args:
    source: Prince_Andrew_of_Greece_and_Denmark
    type: :Man
  AssignClass (2634e3d4-b1a6-417c-a002-98dfb7fa92c8)
 Call ID: 2634e3d4-b1a6-417c-a002-98dfb7fa92c8
  Args:
    source: Princess_Alice_of_Battenberg
    type: :Woman
  AddTriple (9e76902b-42d5-4e4c-b115-7ea25dd75221)
 Call ID: 9e76902b-42d5-4e4c-b115-7ea25dd75221
  Args:
    relation: :hasFather
    target: Prince_Andrew_of_Greece_and_Denmark
    source: Princess_Sophie_of_Greece_and_Denmark
  AddTriple (35cfe0eb-b830-499e-b901-a14f4f9b0977)
 Call ID: 35cfe0eb-b830-499e-b901-a14f4f9b0977
  Args:
    relation: :hasMother
    target: Princess_Alice_of_Battenberg
    source: Princess_Sophie_of_Greece_and_Denmark
  AssignClass (545f145a-68f5-462b-bfa6-903e9d6d5cf9)
 Call ID: 545f145a-68f5-462b-bfa6-903e9d6d5cf9
  Args:
    type: :Man
    source: Prince_Philip_Duke_of_Edinburgh
  AddTriple (38babc11-72eb-4ffa-bfda-10ff460145be)
 Call ID: 38babc11-72eb-4ffa-bfda-10ff460145be
  Args:
    target: Prince_Philip_Duke_of_Edinburgh
    source: Princess_Sophie_of_Greece_and_Denmark
    relation: :isSiblingOf
  Finish (664ffff1-cda3-460f-a2db-b966ea117ba0)
 Call ID: 664ffff1-cda3-460f-a2db-b966ea117ba0
  Args: