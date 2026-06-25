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
Prince Amedeo of Savoy-Aosta, 5th Duke of Aosta (Amedeo Umberto Costantino Giorgio
Early life

Amedeo was born at Villa della Cisterna in Florence, the only child of Prince Aimone, Duke of Aosta, formerly designated king of Croatia as Tomislav II, and of Princess Irene of Greece and Denmark through whom he was a great-great-grandson of Queen Victoria.
When Amedeo was only four years old, his father died in exile in Buenos Aires, and he succeeded him as Duke of Aosta, Prince della Cisterna e Belriguardo, Marchese di Voghera, and Count di Ponderano.
He was an Honorary Companion of the Pennsylvania Commandery of the Military Order of the Loyal Legion of the United States, assigned insignia number 21015, as a great-grandson of Prince Philippe, Count of Paris.
Marriages and family

1st marriage and descendants

On 22 July 1964, at the Igreja Paroquial De São Pedro in Sintra, Portugal, Amedeo married his second cousin, Princess Claude of Orléans (born 11 December 1943).
She was the ninth child and fifth daughter of Henri, comte de Paris, Orléanist claimant to the French throne, and of Princess Isabelle of Orléans-Braganza.
He was involved in various agricultural activities, including the production of wine marketed under the name Vini Savoia Aosta.
Dynastic activities

Amedeo was long viewed by Italian royalists as a likely claimant to the throne if Umberto's own son, Vittorio Emanuele, Prince of Naples, failed to live up to monarchist expectations.
On 7 July 2006, Amedeo declared himself to be the Head of the House of Savoy and Duke of Savoy, claiming that in 1971, Vittorio Emanuele had lost his dynastic rights when he married without previously obtaining the permission of Umberto II, authorization which had been required under monarchical law.
In 2009, Vittorio Emanuele and his son, Emanuele Filiberto, Prince of Venice, sought judicial intervention to forbid Amedeo's use of the surname di Savoia.
In February 2010, the court of Arezzo ruled that the Amedeo and his son Aimone must pay damages totalling 50,000 euros to their cousins and cease using the surname di Savoia instead of di Savoia-Aosta.
Amedeo's claim received the support of Vittorio Emanuele's sister, Princess Maria Gabriella of Savoy.
Although many monarchists transferred their allegiance to Amedeo at some point after King Umberto's death, Amedeo was criticised by other Italian royalists who continue to support Prince Vittorio Emanuele.
But others, including constitutional jurist Guido Locatello, declared the marriage of Vittorio Emanuele to be in violation of Savoy dynastic law years before the scandal evoked any clamour for Amedeo to replace him.
The Unione Monarchica Italiana published in its newsletter, Monarchia Nuova, on 12 February 1987 that the Prince of Naples' marriage to Marina Doria violated the decree of Victor Amadeus III, issued 13 September 1780, regulating the marriages of princes of the blood royal, compelling the Unione to recognise Amedeo as rightful head of the royal house—although at that time Aosta had put forth no public dynastic claim.
Amedeo was a Knight of the Supreme Order of the Most Holy Annunciation named by Umberto II, a Grand Cross of the Order of Saints Maurice and Lazarus named by his cousin Vittorio Emanuele, and a Knight of Honor and Devotion of the Sovereign Military Order of St. John of Jerusalem.
Death

Prince Amedeo died on 1 June 2021, at the age of 77, in Arezzo, Italy, from cardiac arrest after undergoing surgery on 27 May.



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
  AssignClass (c6f88e0a-e18f-40c4-ab63-9a59c15e03e3)
 Call ID: c6f88e0a-e18f-40c4-ab63-9a59c15e03e3
  Args:
    type: :Man
    source: :Amedeo_of_Savoy-Aosta
  AssignClass (33e039ed-fdb2-42a1-8b20-33e97efcf6df)
 Call ID: 33e039ed-fdb2-42a1-8b20-33e97efcf6df
  Args:
    source: :Amedeo_of_Savoy-Aosta
    type: :Person
  AssignClass (942d5be2-8288-41f9-b85a-56b1309444ba)
 Call ID: 942d5be2-8288-41f9-b85a-56b1309444ba
  Args:
    type: :Man
    source: :Aimone_Duke_of_Aosta
  AssignClass (1bf0f9af-374d-462b-a5a1-1bc8f6e5370d)
 Call ID: 1bf0f9af-374d-462b-a5a1-1bc8f6e5370d
  Args:
    source: :Aimone_Duke_of_Aosta
    type: :Person
  AssignClass (88aa77b3-9124-4b25-aa6e-1211ce4bb628)
 Call ID: 88aa77b3-9124-4b25-aa6e-1211ce4bb628
  Args:
    type: :Woman
    source: :Irene_of_Greece_and_Denmark
  AssignClass (cb64f4ec-6837-434a-9846-20acdc15c219)
 Call ID: cb64f4ec-6837-434a-9846-20acdc15c219
  Args:
    type: :Person
    source: :Irene_of_Greece_and_Denmark
  AddTriple (277dc33e-4c66-45aa-9926-ecc9cd848e2b)
 Call ID: 277dc33e-4c66-45aa-9926-ecc9cd848e2b
  Args:
    target: :Aimone_Duke_of_Aosta
    relation: :hasFather
    source: :Amedeo_of_Savoy-Aosta
  AddTriple (014b5c38-3e7d-4c45-9991-02489ca5f424)
 Call ID: 014b5c38-3e7d-4c45-9991-02489ca5f424
  Args:
    relation: :hasMother
    target: :Irene_of_Greece_and_Denmark
    source: :Amedeo_of_Savoy-Aosta
  AssignClass (6957f087-1f07-4f31-924a-df96bf901a98)
 Call ID: 6957f087-1f07-4f31-924a-df96bf901a98
  Args:
    source: :Princess_Claude_of_Orleans
    type: :Woman
  AssignClass (c410b193-4c8e-4e68-8fb5-ab0efc328dd7)
 Call ID: c410b193-4c8e-4e68-8fb5-ab0efc328dd7
  Args:
    type: :Person
    source: :Princess_Claude_of_Orleans
  AddLiteral (d628865e-9400-4202-8f97-d4d2a0deb1da)
 Call ID: d628865e-9400-4202-8f97-d4d2a0deb1da
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1964
    source: :Amedeo_of_Savoy-Aosta
  AddTriple (ea4c3626-ba83-4c44-a60c-f72517bb68c3)
 Call ID: ea4c3626-ba83-4c44-a60c-f72517bb68c3
  Args:
    relation: :hasRelation
    target: :Princess_Claude_of_Orleans
    source: :Amedeo_of_Savoy-Aosta
  AssignClass (030463a2-a035-4bad-a6a8-44da27b85796)
 Call ID: 030463a2-a035-4bad-a6a8-44da27b85796
  Args:
    type: :Man
    source: :Henri_comte_de_Paris
  AssignClass (6016cc69-1b79-4c76-b81b-dc267b7e7eeb)
 Call ID: 6016cc69-1b79-4c76-b81b-dc267b7e7eeb
  Args:
    source: :Henri_comte_de_Paris
    type: :Person
  AssignClass (5bceaa1a-c77a-43e5-a972-875d3e00106f)
 Call ID: 5bceaa1a-c77a-43e5-a972-875d3e00106f
  Args:
    source: :Isabelle_of_Orleans-Braganza
    type: :Woman
  AssignClass (5fcac9bd-4f94-4def-87f0-dba19c7f9705)
 Call ID: 5fcac9bd-4f94-4def-87f0-dba19c7f9705
  Args:
    source: :Isabelle_of_Orleans-Braganza
    type: :Person
  AddTriple (517f4c95-dbcf-4403-adbe-9c1f02c9c992)
 Call ID: 517f4c95-dbcf-4403-adbe-9c1f02c9c992
  Args:
    source: :Princess_Claude_of_Orleans
    target: :Henri_comte_de_Paris
    relation: :hasFather
  AddTriple (3332a8a8-1545-4cac-ab7a-9fb3d473e385)
 Call ID: 3332a8a8-1545-4cac-ab7a-9fb3d473e385
  Args:
    source: :Princess_Claude_of_Orleans
    target: :Isabelle_of_Orleans-Braganza
    relation: :hasMother
  AssignClass (b82bd3d8-f2cb-4a42-be2f-eb8947d793e6)
 Call ID: b82bd3d8-f2cb-4a42-be2f-eb8947d793e6
  Args:
    type: :Man
    source: :Aimone_son_of_Amedeo
  AssignClass (6e9c4fdc-8006-4925-bc19-180d1775229a)
 Call ID: 6e9c4fdc-8006-4925-bc19-180d1775229a
  Args:
    source: :Aimone_son_of_Amedeo
    type: :Person
  AddTriple (fe10805f-bfb6-496d-92b4-ad3fc913cb9b)
 Call ID: fe10805f-bfb6-496d-92b4-ad3fc913cb9b
  Args:
    source: :Aimone_son_of_Amedeo
    target: :Amedeo_of_Savoy-Aosta
    relation: :hasFather
  AssignClass (6a8423e6-2464-49a4-a5f8-6aa76b5a3b80)
 Call ID: 6a8423e6-2464-49a4-a5f8-6aa76b5a3b80
  Args:
    source: :Vittorio_Emanuele_Prince_of_Naples
    type: :Man
  AssignClass (347154fa-2c83-4d37-bbf6-becfba5f1a83)
 Call ID: 347154fa-2c83-4d37-bbf6-becfba5f1a83
  Args:
    source: :Vittorio_Emanuele_Prince_of_Naples
    type: :Person
  AssignClass (599639ba-5953-4f41-a451-a1efd9205884)
 Call ID: 599639ba-5953-4f41-a451-a1efd9205884
  Args:
    type: :Man
    source: :Umberto_II
  AssignClass (f26a19be-5cc9-43a6-9c59-e3e6b6560b4b)
 Call ID: f26a19be-5cc9-43a6-9c59-e3e6b6560b4b
  Args:
    type: :Person
    source: :Umberto_II
  AddTriple (08b076e1-5740-4088-b74b-de4b219bc39e)
 Call ID: 08b076e1-5740-4088-b74b-de4b219bc39e
  Args:
    relation: :hasFather
    target: :Umberto_II
    source: :Vittorio_Emanuele_Prince_of_Naples
  AssignClass (bdc5b6fe-1803-41cd-b65f-5d417dafc027)
 Call ID: bdc5b6fe-1803-41cd-b65f-5d417dafc027
  Args:
    source: :Emanuele_Filiberto_Prince_of_Venice
    type: :Man
  AssignClass (eb18f02f-f2c2-42e0-947e-ebe58a322fb4)
 Call ID: eb18f02f-f2c2-42e0-947e-ebe58a322fb4
  Args:
    source: :Emanuele_Filiberto_Prince_of_Venice
    type: :Person
  AddTriple (1dad435c-24a7-45a8-a793-a7a1b0e0332e)
 Call ID: 1dad435c-24a7-45a8-a793-a7a1b0e0332e
  Args:
    source: :Emanuele_Filiberto_Prince_of_Venice
    target: :Vittorio_Emanuele_Prince_of_Naples
    relation: :hasFather
  AssignClass (eaa2259a-c198-4a21-b143-53c3fa06cb95)
 Call ID: eaa2259a-c198-4a21-b143-53c3fa06cb95
  Args:
    source: :Maria_Gabriella_of_Savoy
    type: :Woman
  AssignClass (b7447816-ae81-499b-a079-ca3f075ff2bf)
 Call ID: b7447816-ae81-499b-a079-ca3f075ff2bf
  Args:
    source: :Maria_Gabriella_of_Savoy
    type: :Person
  AddTriple (0b6d698c-e78a-493f-86cf-0c29de361b48)
 Call ID: 0b6d698c-e78a-493f-86cf-0c29de361b48
  Args:
    source: :Maria_Gabriella_of_Savoy
    target: :Umberto_II
    relation: :hasFather
  AddLiteral (78d55795-7e4b-4019-9034-9c80550659d9)
 Call ID: 78d55795-7e4b-4019-9034-9c80550659d9
  Args:
    literal_type: xsd:integer
    source: :Amedeo_of_Savoy-Aosta
    literal_value: 2021
    relation: :hasDeathYear
  Finish (d74978f3-f93c-40c7-909d-4af7675e5150)
 Call ID: d74978f3-f93c-40c7-909d-4af7675e5150
  Args: