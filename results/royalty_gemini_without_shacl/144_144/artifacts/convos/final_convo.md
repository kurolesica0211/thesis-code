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
  AssignClass (19375b49-5358-40c9-a76f-b5ce23386b2d)
 Call ID: 19375b49-5358-40c9-a76f-b5ce23386b2d
  Args:
    source: :Prince_Christoph_of_Hesse
    type: :Man
  AssignClass (624d97dc-1e45-425a-af9f-6dcedb28c2ff)
 Call ID: 624d97dc-1e45-425a-af9f-6dcedb28c2ff
  Args:
    source: :Prince_Christoph_of_Hesse
    type: :Person
  AddLiteral (a3e3b729-c163-439a-baed-246275be6670)
 Call ID: a3e3b729-c163-439a-baed-246275be6670
  Args:
    source: :Prince_Christoph_of_Hesse
    relation: :hasBirthYear
    literal_value: 1901
    literal_type: xsd:integer
  AddLiteral (06b89853-cc88-4f79-96ae-3cd901c9c622)
 Call ID: 06b89853-cc88-4f79-96ae-3cd901c9c622
  Args:
    literal_type: xsd:integer
    literal_value: 1943
    relation: :hasDeathYear
    source: :Prince_Christoph_of_Hesse
  AssignClass (570b6983-45b3-49a4-9d5b-39809dec58fd)
 Call ID: 570b6983-45b3-49a4-9d5b-39809dec58fd
  Args:
    source: :Kaiser_Wilhelm_II
    type: :Man
  AssignClass (99095dee-86e1-464b-8eb9-9012edff0979)
 Call ID: 99095dee-86e1-464b-8eb9-9012edff0979
  Args:
    type: :Person
    source: :Kaiser_Wilhelm_II
  AddTriple (ed8f59e2-71d0-43bf-804e-70b6af09e91a)
 Call ID: ed8f59e2-71d0-43bf-804e-70b6af09e91a
  Args:
    source: :Prince_Christoph_of_Hesse
    relation: :hasRelation
    target: :Kaiser_Wilhelm_II
  AssignClass (e05d0b81-79d7-4125-8bab-d3a8578cf1d8)
 Call ID: e05d0b81-79d7-4125-8bab-d3a8578cf1d8
  Args:
    source: :Prince_Philip_of_Greece_and_Denmark
    type: :Man
  AssignClass (9a443023-2076-4de9-aecc-151605c72c40)
 Call ID: 9a443023-2076-4de9-aecc-151605c72c40
  Args:
    source: :Prince_Philip_of_Greece_and_Denmark
    type: :Person
  AddTriple (3991e05f-e751-4c32-8e76-a9dddd6aae34)
 Call ID: 3991e05f-e751-4c32-8e76-a9dddd6aae34
  Args:
    source: :Princess_Sophie_of_Greece_and_Denmark
    relation: :isBrotherOf
    target: :Prince_Philip_of_Greece_and_Denmark
  AssignClass (cd5a1957-c7c3-4813-bb36-959500848ad0)
 Call ID: cd5a1957-c7c3-4813-bb36-959500848ad0
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AssignClass (d54a2a91-12a8-4e68-a393-8ced878e0a2f)
 Call ID: d54a2a91-12a8-4e68-a393-8ced878e0a2f
  Args:
    type: :Person
    source: :Queen_Elizabeth_II
  AssignClass (c68677bc-14d8-439d-b04c-7f730d0a70c5)
 Call ID: c68677bc-14d8-439d-b04c-7f730d0a70c5
  Args:
    type: :Man
    source: :Prince_Frederick_Charles_of_Hesse
  AssignClass (e30a2811-101c-40d4-adb8-f0b32facafe4)
 Call ID: e30a2811-101c-40d4-adb8-f0b32facafe4
  Args:
    type: :Person
    source: :Prince_Frederick_Charles_of_Hesse
  AssignClass (d5ab8cd2-dff5-42ad-87f9-f53dd5fb6aad)
 Call ID: d5ab8cd2-dff5-42ad-87f9-f53dd5fb6aad
  Args:
    type: :Woman
    source: :Princess_Margaret_of_Prussia
  AssignClass (cb40b77d-d51d-4c7c-b593-2d99dedf214c)
 Call ID: cb40b77d-d51d-4c7c-b593-2d99dedf214c
  Args:
    source: :Princess_Margaret_of_Prussia
    type: :Person
  AddTriple (b9668ea6-bf0f-48db-840d-047fe3a7d551)
 Call ID: b9668ea6-bf0f-48db-840d-047fe3a7d551
  Args:
    source: :Prince_Christoph_of_Hesse
    relation: :hasFather
    target: :Prince_Frederick_Charles_of_Hesse
  AddTriple (0ffb8d17-1308-4f67-bca1-5d44c8b40362)
 Call ID: 0ffb8d17-1308-4f67-bca1-5d44c8b40362
  Args:
    relation: :hasMother
    target: :Princess_Margaret_of_Prussia
    source: :Prince_Christoph_of_Hesse
  AssignClass (ab679824-b2c6-47d3-9f04-65b6590fa2fc)
 Call ID: ab679824-b2c6-47d3-9f04-65b6590fa2fc
  Args:
    source: :Prince_Richard_of_Hesse
    type: :Man
  AssignClass (1fd204a4-b795-44f9-8eb2-90a62c9ddcca)
 Call ID: 1fd204a4-b795-44f9-8eb2-90a62c9ddcca
  Args:
    type: :Person
    source: :Prince_Richard_of_Hesse
  AddTriple (82f436c8-957f-498b-a6ba-84bf57156213)
 Call ID: 82f436c8-957f-498b-a6ba-84bf57156213
  Args:
    target: :Prince_Richard_of_Hesse
    relation: :isSiblingOf
    source: :Prince_Christoph_of_Hesse
  AssignClass (c81882ab-8e84-44d1-87d2-548bf7a9806f)
 Call ID: c81882ab-8e84-44d1-87d2-548bf7a9806f
  Args:
    source: :Emperor_Frederick_III
    type: :Man
  AssignClass (45ef12e5-0afb-4556-a3b5-4b743a6b8cc4)
 Call ID: 45ef12e5-0afb-4556-a3b5-4b743a6b8cc4
  Args:
    type: :Person
    source: :Emperor_Frederick_III
  AssignClass (97910b2f-d9d9-4181-bdc3-c5f33d414c63)
 Call ID: 97910b2f-d9d9-4181-bdc3-c5f33d414c63
  Args:
    source: :Victoria_Princess_Royal
    type: :Woman
  AssignClass (c8e5a184-86d1-429c-a850-fce228783654)
 Call ID: c8e5a184-86d1-429c-a850-fce228783654
  Args:
    type: :Person
    source: :Victoria_Princess_Royal
  AddTriple (76ee4108-8349-4cd0-87a3-1e5cb437b64d)
 Call ID: 76ee4108-8349-4cd0-87a3-1e5cb437b64d
  Args:
    relation: :hasFather
    target: :Emperor_Frederick_III
    source: :Princess_Margaret_of_Prussia
  AddTriple (2b74e71a-35d6-44ac-a746-f8b70742d233)
 Call ID: 2b74e71a-35d6-44ac-a746-f8b70742d233
  Args:
    relation: :hasMother
    target: :Victoria_Princess_Royal
    source: :Princess_Margaret_of_Prussia
  AssignClass (f1aa259f-dffd-42cc-9299-2d21216b9919)
 Call ID: f1aa259f-dffd-42cc-9299-2d21216b9919
  Args:
    type: :Woman
    source: :Queen_Victoria
  AssignClass (ef3b2c4b-dc16-4754-a4f5-57b440ab8f95)
 Call ID: ef3b2c4b-dc16-4754-a4f5-57b440ab8f95
  Args:
    source: :Queen_Victoria
    type: :Person
  AssignClass (6cbf4d7e-1df8-4f3b-bf45-ae202d47e631)
 Call ID: 6cbf4d7e-1df8-4f3b-bf45-ae202d47e631
  Args:
    source: :Prince_Albert_of_Saxe_Coburg_and_Gotha
    type: :Man
  AssignClass (2bcf2b28-509b-458a-8f22-ebc913c6ff75)
 Call ID: 2bcf2b28-509b-458a-8f22-ebc913c6ff75
  Args:
    source: :Prince_Albert_of_Saxe_Coburg_and_Gotha
    type: :Person
  AssignClass (608b412f-47af-4504-86cf-4b44e7afe453)
 Call ID: 608b412f-47af-4504-86cf-4b44e7afe453
  Args:
    type: :Man
    source: :Prince_Philipp_of_Hesse
  AssignClass (680c9acf-18c8-4fc0-9875-c1d4f220badb)
 Call ID: 680c9acf-18c8-4fc0-9875-c1d4f220badb
  Args:
    type: :Person
    source: :Prince_Philipp_of_Hesse
  AssignClass (0310ee44-8a79-4d5d-80f5-44748b669ecb)
 Call ID: 0310ee44-8a79-4d5d-80f5-44748b669ecb
  Args:
    source: :Prince_Wolfgang_of_Hesse
    type: :Man
  AssignClass (ac34916a-0be9-4e24-93a9-c9636e7f6ac6)
 Call ID: ac34916a-0be9-4e24-93a9-c9636e7f6ac6
  Args:
    source: :Prince_Wolfgang_of_Hesse
    type: :Person
  AssignClass (783ef3c6-4b74-46af-8895-c21138095e88)
 Call ID: 783ef3c6-4b74-46af-8895-c21138095e88
  Args:
    type: :Man
    source: :Friedrich_Wilhelm_of_Hesse
  AssignClass (14232d41-ca12-4823-86a9-3b6c61fbf0cc)
 Call ID: 14232d41-ca12-4823-86a9-3b6c61fbf0cc
  Args:
    type: :Person
    source: :Friedrich_Wilhelm_of_Hesse
  AssignClass (41a7f675-d40c-4723-8854-4861df3d3602)
 Call ID: 41a7f675-d40c-4723-8854-4861df3d3602
  Args:
    type: :Man
    source: :Maximilian_of_Hesse
  AssignClass (edd181b8-5aff-42fa-8149-bb70e7312ce6)
 Call ID: edd181b8-5aff-42fa-8149-bb70e7312ce6
  Args:
    source: :Maximilian_of_Hesse
    type: :Person
  AddTriple (8e743200-6a79-425b-8b16-e4cb36db6ac1)
 Call ID: 8e743200-6a79-425b-8b16-e4cb36db6ac1
  Args:
    relation: :isSiblingOf
    target: :Prince_Philipp_of_Hesse
    source: :Prince_Christoph_of_Hesse
  AddTriple (b1e503cb-bbf2-4fa7-b7ce-3cd87a21479f)
 Call ID: b1e503cb-bbf2-4fa7-b7ce-3cd87a21479f
  Args:
    relation: :isSiblingOf
    target: :Prince_Wolfgang_of_Hesse
    source: :Prince_Christoph_of_Hesse
  AddTriple (f6275244-cd13-4019-aae5-a82c604cb61d)
 Call ID: f6275244-cd13-4019-aae5-a82c604cb61d
  Args:
    relation: :isSiblingOf
    target: :Friedrich_Wilhelm_of_Hesse
    source: :Prince_Christoph_of_Hesse
  AddTriple (790d3cca-910e-4d91-9e95-b91372b95f5d)
 Call ID: 790d3cca-910e-4d91-9e95-b91372b95f5d
  Args:
    source: :Prince_Christoph_of_Hesse
    target: :Maximilian_of_Hesse
    relation: :isSiblingOf
  AssignClass (c75c30bf-d86b-4532-8a1c-94b0c8bce563)
 Call ID: c75c30bf-d86b-4532-8a1c-94b0c8bce563
  Args:
    type: :Woman
    source: :Princess_Sophie_of_Greece_and_Denmark
  AssignClass (8d08d81f-e87e-4f43-a042-a80d217ab3c5)
 Call ID: 8d08d81f-e87e-4f43-a042-a80d217ab3c5
  Args:
    type: :Person
    source: :Princess_Sophie_of_Greece_and_Denmark
  AddTriple (60389b23-a2e2-47b0-94b7-ff147dd20041)
 Call ID: 60389b23-a2e2-47b0-94b7-ff147dd20041
  Args:
    relation: :hasMarriageYear
    target: :Princess_Sophie_of_Greece_and_Denmark
    source: :Prince_Christoph_of_Hesse
  AddLiteral (1b87871c-cfa5-4946-98fa-5082a9e8b30a)
 Call ID: 1b87871c-cfa5-4946-98fa-5082a9e8b30a
  Args:
    literal_type: xsd:integer
    literal_value: 1930
    relation: :hasMarriageYear
    source: :Prince_Christoph_of_Hesse
  AssignClass (aee66e4d-f677-4ba2-9620-868d4c38f23c)
 Call ID: aee66e4d-f677-4ba2-9620-868d4c38f23c
  Args:
    type: :Man
    source: :Prince_Andrew_of_Greece_and_Denmark
  AssignClass (befe72d3-cf72-4e2c-a964-a371150cad5e)
 Call ID: befe72d3-cf72-4e2c-a964-a371150cad5e
  Args:
    type: :Person
    source: :Prince_Andrew_of_Greece_and_Denmark
  AssignClass (fd9b2e69-8564-4fa7-8aac-243255c5e378)
 Call ID: fd9b2e69-8564-4fa7-8aac-243255c5e378
  Args:
    type: :Woman
    source: :Princess_Alice_of_Battenberg
  AssignClass (6ab80010-fb3a-43f0-b435-e82676614ef8)
 Call ID: 6ab80010-fb3a-43f0-b435-e82676614ef8
  Args:
    type: :Person
    source: :Princess_Alice_of_Battenberg
  AddTriple (5e132e13-8193-4ef5-93aa-61fd6b678fee)
 Call ID: 5e132e13-8193-4ef5-93aa-61fd6b678fee
  Args:
    relation: :hasFather
    target: :Prince_Andrew_of_Greece_and_Denmark
    source: :Princess_Sophie_of_Greece_and_Denmark
  AddTriple (2225dc5e-f237-41ae-9896-f1e15ce36fdb)
 Call ID: 2225dc5e-f237-41ae-9896-f1e15ce36fdb
  Args:
    target: :Princess_Alice_of_Battenberg
    relation: :hasMother
    source: :Princess_Sophie_of_Greece_and_Denmark
  AssignClass (baccf039-eefc-4cb5-a064-f1f105531324)
 Call ID: baccf039-eefc-4cb5-a064-f1f105531324
  Args:
    source: :Prince_George_William_of_Hanover
    type: :Man
  AssignClass (53705a12-b62a-414f-b335-55142055d800)
 Call ID: 53705a12-b62a-414f-b335-55142055d800
  Args:
    source: :Prince_George_William_of_Hanover
    type: :Person
  AssignClass (1d851e80-0ce8-4bca-9495-db65f4e32fc6)
 Call ID: 1d851e80-0ce8-4bca-9495-db65f4e32fc6
  Args:
    type: :Woman
    source: :Queen_Fredrica_of_Greece
  AssignClass (97ecb2a2-f089-4643-bcec-a317d3567cb2)
 Call ID: 97ecb2a2-f089-4643-bcec-a317d3567cb2
  Args:
    type: :Person
    source: :Queen_Fredrica_of_Greece
  AddTriple (6c7b2f13-5a8f-4f11-8660-ca201ad3241a)
 Call ID: 6c7b2f13-5a8f-4f11-8660-ca201ad3241a
  Args:
    target: :Queen_Fredrica_of_Greece
    relation: :isSiblingOf
    source: :Prince_George_William_of_Hanover
  AssignClass (b2dfcb30-ed52-47c3-9171-ff8f496abbca)
 Call ID: b2dfcb30-ed52-47c3-9171-ff8f496abbca
  Args:
    type: :Man
    source: :King_Charles_III
  AssignClass (d156378f-4815-4ba5-b668-4cdd47bc575d)
 Call ID: d156378f-4815-4ba5-b668-4cdd47bc575d
  Args:
    source: :King_Charles_III
    type: :Person
  Finish (c5f74089-d559-4017-98c8-afba8d53f848)
 Call ID: c5f74089-d559-4017-98c8-afba8d53f848
  Args: