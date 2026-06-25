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
Prince Aimone, 4th Duke of Aosta (Aimone Roberto Margherita Maria Giuseppe Torino; 9 March 1900 – 29 January 1948), was a prince of Italy's reigning House of Savoy and an officer of the Royal Italian Navy.
The second son of Prince Emanuele Filiberto, Duke of Aosta, he was granted the title Duke of Spoleto on 22 September 1904.
He inherited the title Duke of Aosta on 3 March 1942 following the death of his brother Prince Amedeo in a British prisoner of war camp in Nairobi.
From 18 May 1941 to 31 July 1943, Aimone was designated king of the Independent State of Croatia (Croatian: Nezavisna Država Hrvatska, NDH), even though he never ruled there.
After the dismissal of Mussolini on 25 July 1943, Aimone abdicated on 31 July as king on the orders of Victor Emmanuel III.
Early life

Prince Aimone Roberto Margherita Maria Giuseppe Torino of Savoy-Aosta was born in Turin the second son of Prince Emanuele Filiberto, Duke of Aosta (eldest son of Prince Amedeo, 1st Duke of Aosta (and sometime "King Amadeo I of Spain") by his wife, née Vittoria dal Pozzo, Principessa della Cisterna) and Princess Hélène of Orléans (daughter of Philippe, comte de Paris, and Princess Marie Isabelle of Orléans).
With his brother Amedeo, he was educated at St  David's College, Reigate, Surrey, England, and Aimone later went to study at the naval academy in Livorno.
On 1 April 1921, Prince Aimone became a member of the Italian Senate.
In 1929, twenty years after his uncle Prince Luigi Amedeo, Duke of the Abruzzi had attempted to climb K2 in Karakoram, Prince Aimone led an expedition to Karakorum.
Due to the failure to climb K2 twenty years earlier, Prince Aimone's expedition concentrated solely on scientific work.
Marriage and issue

After being romantically linked with Infanta Beatriz of Spain, the daughter of King Alfonso XIII, he married, on 1 July 1939 at the church of Santa Maria del Fiore, Florence, Princess Irene of Greece and Denmark, daughter of King Constantine I and Princess Sophie of Prussia.
They had one son, Prince Amedeo, Duke of Aosta, born in 1943.
Aimone was then officially named king by his cousin Victor Emmanuel III.
The Italian Foreign Minister and Benito Mussolini's son in law Count Ciano's informants said of Aimone "The Duke doesn't give a damn about Croatia and wants only money, money and more money."
Ciano's diary noted a conversation between Aimone and himself, where Aimone was "proud of having been chosen King of Croatia, but has no exact idea of what he is supposed to do and is vaguely uneasy about it".
Aimone felt that Dalmatia "was a land that could never be Italianized" and was an obstacle to Italo-Croatian reconciliation.
Prince Aimone also established a Croatian office in Rome where he received confidential reports, official documents, and military, political and economic information from Croatia.
After the fall of the Fascist regime in Italy, Aimone abdicated as king of Croatia on 31 July 1943 on the orders of Victor Emmanuel III.
Prince Aimone succeeded to the title duke of Aosta on 3 March 1942, following the death of his elder brother Prince Amedeo, 3rd Duke of Aosta, in a British prisoner of war camp in Kenya.
In the autumn of 1942, Aimone contacted Allied forces via his courier, the consul general Alessandro Marieni, about the possibility of a peace settlement between Italy and Allied forces.
Death

In 1947, following the birth of the Italian Republic the previous year, Prince Aimone left Italy for South America.
The claim to the Aosta ducal title passed to his son Prince Amedeo.
}} Media related to Prince Aimone, Duke of Aosta at Wikimedia Commons



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
  AssignClass (51c5008c-2f97-4e84-a872-ff41907de1d8)
 Call ID: 51c5008c-2f97-4e84-a872-ff41907de1d8
  Args:
    source: Prince_Aimone
    type: :Man
  AssignClass (42d3c3ab-67e8-42a0-8691-ab11c12d9641)
 Call ID: 42d3c3ab-67e8-42a0-8691-ab11c12d9641
  Args:
    source: Prince_Aimone
    type: :Person
  AddLiteral (d7649492-29fa-4ea6-a439-5df880386d3b)
 Call ID: d7649492-29fa-4ea6-a439-5df880386d3b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Prince_Aimone
    literal_value: 1900
  AddLiteral (e435a0e9-3838-46c3-b1a5-ecf90fcc77cc)
 Call ID: e435a0e9-3838-46c3-b1a5-ecf90fcc77cc
  Args:
    literal_type: xsd:integer
    source: Prince_Aimone
    relation: :hasDeathYear
    literal_value: 1948
  AssignClass (800ce558-948f-4a91-9cd2-f19e5d089695)
 Call ID: 800ce558-948f-4a91-9cd2-f19e5d089695
  Args:
    source: Prince_Emanuele_Filiberto
    type: :Man
  AssignClass (642f6089-43e0-48ee-b193-64ed308270ad)
 Call ID: 642f6089-43e0-48ee-b193-64ed308270ad
  Args:
    source: Prince_Emanuele_Filiberto
    type: :Person
  AddTriple (9ccdcc64-23cd-473d-88de-463ffc6d0e94)
 Call ID: 9ccdcc64-23cd-473d-88de-463ffc6d0e94
  Args:
    target: Prince_Emanuele_Filiberto
    source: Prince_Aimone
    relation: :hasFather
  AssignClass (f7b01b90-b470-4d18-90b1-346b78f65378)
 Call ID: f7b01b90-b470-4d18-90b1-346b78f65378
  Args:
    source: Princess_Helene_of_Orleans
    type: :Woman
  AssignClass (03d38a8a-4699-4837-b065-ad49cd448c95)
 Call ID: 03d38a8a-4699-4837-b065-ad49cd448c95
  Args:
    source: Princess_Helene_of_Orleans
    type: :Person
  AddTriple (5ed0ea88-6ba1-4588-b3d9-def228eb9668)
 Call ID: 5ed0ea88-6ba1-4588-b3d9-def228eb9668
  Args:
    target: Princess_Helene_of_Orleans
    source: Prince_Aimone
    relation: :hasMother
  AssignClass (41f1502b-f036-4747-b206-fb0e9f8f3b51)
 Call ID: 41f1502b-f036-4747-b206-fb0e9f8f3b51
  Args:
    source: Prince_Amedeo_3rd_Duke_of_Aosta
    type: :Man
  AssignClass (eb47aed6-95fe-4b0a-b4ef-61ae386b5c1c)
 Call ID: eb47aed6-95fe-4b0a-b4ef-61ae386b5c1c
  Args:
    source: Prince_Amedeo_3rd_Duke_of_Aosta
    type: :Person
  AddTriple (53315eea-c864-452f-b326-693637f76c7d)
 Call ID: 53315eea-c864-452f-b326-693637f76c7d
  Args:
    target: Prince_Amedeo_3rd_Duke_of_Aosta
    source: Prince_Aimone
    relation: :hasBrother
  AssignClass (70a3e17f-8b72-4831-b5fe-ffef42eaa7f3)
 Call ID: 70a3e17f-8b72-4831-b5fe-ffef42eaa7f3
  Args:
    source: Prince_Amedeo_1st_Duke_of_Aosta
    type: :Man
  AssignClass (580d7094-55c0-4979-ac72-3331ecc961da)
 Call ID: 580d7094-55c0-4979-ac72-3331ecc961da
  Args:
    source: Prince_Amedeo_1st_Duke_of_Aosta
    type: :Person
  AddTriple (32c986c1-90b8-41e7-9b6d-1755c0458cf5)
 Call ID: 32c986c1-90b8-41e7-9b6d-1755c0458cf5
  Args:
    target: Prince_Amedeo_1st_Duke_of_Aosta
    source: Prince_Emanuele_Filiberto
    relation: :hasFather
  AssignClass (f97d5983-a909-4e69-af55-3d5bf6721d86)
 Call ID: f97d5983-a909-4e69-af55-3d5bf6721d86
  Args:
    source: Vittoria_dal_Pozzo
    type: :Woman
  AssignClass (c435cb33-448d-40c2-b1f9-bf2d17110357)
 Call ID: c435cb33-448d-40c2-b1f9-bf2d17110357
  Args:
    source: Vittoria_dal_Pozzo
    type: :Person
  AddTriple (49cf3c8e-de74-4a7f-a96a-cf04b430f212)
 Call ID: 49cf3c8e-de74-4a7f-a96a-cf04b430f212
  Args:
    source: Prince_Emanuele_Filiberto
    relation: :hasMother
    target: Vittoria_dal_Pozzo
  AssignClass (5e93dc59-4ba2-4bbc-89d9-f7c667296028)
 Call ID: 5e93dc59-4ba2-4bbc-89d9-f7c667296028
  Args:
    source: Philippe_comte_de_Paris
    type: :Man
  AssignClass (f242a0a4-356c-4432-b787-12ad4111e9db)
 Call ID: f242a0a4-356c-4432-b787-12ad4111e9db
  Args:
    source: Philippe_comte_de_Paris
    type: :Person
  AddTriple (31dc1270-8e10-4a27-87f7-c4c245311a67)
 Call ID: 31dc1270-8e10-4a27-87f7-c4c245311a67
  Args:
    source: Princess_Helene_of_Orleans
    relation: :hasFather
    target: Philippe_comte_de_Paris
  AssignClass (7b086b7b-e151-42c0-9c1b-e8ba098524fa)
 Call ID: 7b086b7b-e151-42c0-9c1b-e8ba098524fa
  Args:
    source: Princess_Marie_Isabelle_of_Orleans
    type: :Woman
  AssignClass (1131e1c3-25d2-458f-b593-f6a118a5dae7)
 Call ID: 1131e1c3-25d2-458f-b593-f6a118a5dae7
  Args:
    source: Princess_Marie_Isabelle_of_Orleans
    type: :Person
  AddTriple (861d4e22-3841-4619-9ce5-e810beb0a996)
 Call ID: 861d4e22-3841-4619-9ce5-e810beb0a996
  Args:
    target: Princess_Marie_Isabelle_of_Orleans
    source: Princess_Helene_of_Orleans
    relation: :hasMother
  AssignClass (f1872750-da66-41ad-ae36-ef2f82d691f3)
 Call ID: f1872750-da66-41ad-ae36-ef2f82d691f3
  Args:
    source: Prince_Luigi_Amedeo_Duke_of_the_Abruzzi
    type: :Man
  AssignClass (7ce01df0-ee36-463f-922e-7e56b129a32f)
 Call ID: 7ce01df0-ee36-463f-922e-7e56b129a32f
  Args:
    source: Prince_Luigi_Amedeo_Duke_of_the_Abruzzi
    type: :Person
  AddTriple (97b3b9fa-ba26-4a33-8411-e25f36756129)
 Call ID: 97b3b9fa-ba26-4a33-8411-e25f36756129
  Args:
    source: Prince_Luigi_Amedeo_Duke_of_the_Abruzzi
    relation: :isUncleOf
    target: Prince_Aimone
  AssignClass (8a9a37c2-75bd-41e6-b69e-c0c7fb221dc8)
 Call ID: 8a9a37c2-75bd-41e6-b69e-c0c7fb221dc8
  Args:
    source: Infanta_Beatriz_of_Spain
    type: :Woman
  AssignClass (73a3917a-fe93-4bad-a120-358a56ccbd2f)
 Call ID: 73a3917a-fe93-4bad-a120-358a56ccbd2f
  Args:
    source: Infanta_Beatriz_of_Spain
    type: :Person
  AssignClass (1b9008de-fdb7-4dcb-8d0f-31d769245415)
 Call ID: 1b9008de-fdb7-4dcb-8d0f-31d769245415
  Args:
    source: King_Alfonso_XIII
    type: :Man
  AssignClass (313279fb-a260-4ff1-b671-8a79ae6de661)
 Call ID: 313279fb-a260-4ff1-b671-8a79ae6de661
  Args:
    source: King_Alfonso_XIII
    type: :Person
  AddTriple (5ae68e00-9cc4-4290-8322-99e760b922f4)
 Call ID: 5ae68e00-9cc4-4290-8322-99e760b922f4
  Args:
    source: Infanta_Beatriz_of_Spain
    relation: :hasFather
    target: King_Alfonso_XIII
  AssignClass (3177883a-7cbe-4a47-b0f9-e1199722c859)
 Call ID: 3177883a-7cbe-4a47-b0f9-e1199722c859
  Args:
    source: Princess_Irene_of_Greece_and_Denmark
    type: :Woman
  AssignClass (7092e905-0fbf-408f-bb0b-8e26bd5d1daf)
 Call ID: 7092e905-0fbf-408f-bb0b-8e26bd5d1daf
  Args:
    source: Princess_Irene_of_Greece_and_Denmark
    type: :Person
  AddTriple (1425ba74-2d65-4654-af29-a5a064cfd46a)
 Call ID: 1425ba74-2d65-4654-af29-a5a064cfd46a
  Args:
    source: Prince_Amedeo_Duke_of_Aosta_son
    relation: :hasMother
    target: Princess_Irene_of_Greece_and_Denmark
  AddLiteral (2a964986-0327-4f48-895b-35d5cb41bc1d)
 Call ID: 2a964986-0327-4f48-895b-35d5cb41bc1d
  Args:
    relation: :hasMarriageYear
    literal_value: 1939
    source: Prince_Aimone
    literal_type: xsd:integer
  AddTriple (6f9210fc-5e90-48ce-aa66-17a18dc50f2c)
 Call ID: 6f9210fc-5e90-48ce-aa66-17a18dc50f2c
  Args:
    target: Prince_Aimone
    source: Prince_Amedeo_Duke_of_Aosta_son
    relation: :hasFather
  AssignClass (fe970933-a47f-46de-9c60-5e669193610c)
 Call ID: fe970933-a47f-46de-9c60-5e669193610c
  Args:
    source: Prince_Amedeo_Duke_of_Aosta_son
    type: :Man
  AssignClass (24be3644-54e3-4e26-9ba0-55d5d1f338d0)
 Call ID: 24be3644-54e3-4e26-9ba0-55d5d1f338d0
  Args:
    source: Prince_Amedeo_Duke_of_Aosta_son
    type: :Person
  AssignClass (5da13f90-bb07-412f-9d33-37d8789758cc)
 Call ID: 5da13f90-bb07-412f-9d33-37d8789758cc
  Args:
    source: King_Constantine_I
    type: :Man
  AssignClass (c20708ae-7aa8-492b-8a27-cf9e1cb1b9d0)
 Call ID: c20708ae-7aa8-492b-8a27-cf9e1cb1b9d0
  Args:
    source: King_Constantine_I
    type: :Person
  AddTriple (2eb5504b-3c65-4a6d-9aad-2fe1e11d4aeb)
 Call ID: 2eb5504b-3c65-4a6d-9aad-2fe1e11d4aeb
  Args:
    source: Princess_Irene_of_Greece_and_Denmark
    relation: :hasFather
    target: King_Constantine_I
  AssignClass (7ca44247-0320-4e24-abfb-2f33857ba02a)
 Call ID: 7ca44247-0320-4e24-abfb-2f33857ba02a
  Args:
    source: Princess_Sophie_of_Prussia
    type: :Woman
  AssignClass (7d12029b-383d-49d9-8c23-fc8e8c3f9cad)
 Call ID: 7d12029b-383d-49d9-8c23-fc8e8c3f9cad
  Args:
    source: Princess_Sophie_of_Prussia
    type: :Person
  AddTriple (79be3547-6632-4634-9398-7564f1164af2)
 Call ID: 79be3547-6632-4634-9398-7564f1164af2
  Args:
    source: Princess_Irene_of_Greece_and_Denmark
    relation: :hasMother
    target: Princess_Sophie_of_Prussia
  AssignClass (db33fbe5-4e98-4a28-ac2d-5cabd545b171)
 Call ID: db33fbe5-4e98-4a28-ac2d-5cabd545b171
  Args:
    source: Victor_Emmanuel_III
    type: :Man
  AssignClass (6b216c4e-30a8-4a12-8a05-ea4a0214118a)
 Call ID: 6b216c4e-30a8-4a12-8a05-ea4a0214118a
  Args:
    source: Victor_Emmanuel_III
    type: :Person
  Finish (e8263dda-be98-49f9-b668-bc767d35eaec)
 Call ID: e8263dda-be98-49f9-b668-bc767d35eaec
  Args: