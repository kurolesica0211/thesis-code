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
  AssignClass (9c0d8e1a-b3eb-428d-8593-b88c4b77b8bc)
 Call ID: 9c0d8e1a-b3eb-428d-8593-b88c4b77b8bc
  Args:
    type: :Man
    source: Prince_Aimone
  AssignClass (e27236d8-5b60-4239-a37c-673aaac0d9a1)
 Call ID: e27236d8-5b60-4239-a37c-673aaac0d9a1
  Args:
    type: :Person
    source: Prince_Aimone
  AddLiteral (3e978c1c-5012-4662-8a79-f45d5de88c48)
 Call ID: 3e978c1c-5012-4662-8a79-f45d5de88c48
  Args:
    source: Prince_Aimone
    literal_value: 1900
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (951998c9-57a9-462d-8dcd-0181abd23f65)
 Call ID: 951998c9-57a9-462d-8dcd-0181abd23f65
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Aimone
    literal_value: 1948
  AssignClass (8511c66a-57dc-4f0b-a567-ab659fdfbbf4)
 Call ID: 8511c66a-57dc-4f0b-a567-ab659fdfbbf4
  Args:
    type: :Man
    source: Prince_Emanuele_Filiberto
  AssignClass (65b06f89-2d45-4d2e-bb65-12e2d4bae362)
 Call ID: 65b06f89-2d45-4d2e-bb65-12e2d4bae362
  Args:
    type: :Person
    source: Prince_Emanuele_Filiberto
  AddTriple (c14296fb-058e-427e-9b4a-a7081770bad6)
 Call ID: c14296fb-058e-427e-9b4a-a7081770bad6
  Args:
    target: Prince_Emanuele_Filiberto
    relation: :hasFather
    source: Prince_Aimone
  AssignClass (ca867f24-442f-48dd-885b-1012b9402cc2)
 Call ID: ca867f24-442f-48dd-885b-1012b9402cc2
  Args:
    type: :Woman
    source: Princess_Helene_of_Orleans
  AssignClass (fba784a7-a01e-4701-8a00-712a817aa09a)
 Call ID: fba784a7-a01e-4701-8a00-712a817aa09a
  Args:
    type: :Person
    source: Princess_Helene_of_Orleans
  AddTriple (1d8200e2-99f6-405d-8f02-26eaaba8ddb4)
 Call ID: 1d8200e2-99f6-405d-8f02-26eaaba8ddb4
  Args:
    source: Prince_Aimone
    relation: :hasMother
    target: Princess_Helene_of_Orleans
  AssignClass (35300bd7-53b6-4bd1-8527-8ec4af7a92fc)
 Call ID: 35300bd7-53b6-4bd1-8527-8ec4af7a92fc
  Args:
    type: :Man
    source: Prince_Amedeo_3rd_Duke_of_Aosta
  AssignClass (8e0e53dd-aed8-40c9-83a3-db6fe7a7aaf0)
 Call ID: 8e0e53dd-aed8-40c9-83a3-db6fe7a7aaf0
  Args:
    type: :Person
    source: Prince_Amedeo_3rd_Duke_of_Aosta
  AddTriple (d6d8001c-e60a-4316-a40d-2d857141e895)
 Call ID: d6d8001c-e60a-4316-a40d-2d857141e895
  Args:
    target: Prince_Amedeo_3rd_Duke_of_Aosta
    relation: :isBrotherOf
    source: Prince_Aimone
  AssignClass (3ab66bd2-fc31-40db-aedb-de2a10637352)
 Call ID: 3ab66bd2-fc31-40db-aedb-de2a10637352
  Args:
    type: :Man
    source: Prince_Amedeo_1st_Duke_of_Aosta
  AssignClass (f309c6a0-7a4a-4b40-9737-437ed3d64833)
 Call ID: f309c6a0-7a4a-4b40-9737-437ed3d64833
  Args:
    type: :Person
    source: Prince_Amedeo_1st_Duke_of_Aosta
  AddTriple (a3d53d2c-de70-440e-8653-66b98cff7676)
 Call ID: a3d53d2c-de70-440e-8653-66b98cff7676
  Args:
    target: Prince_Amedeo_1st_Duke_of_Aosta
    relation: :hasFather
    source: Prince_Emanuele_Filiberto
  AssignClass (6bfe147b-7d0a-4ba1-8f1e-49758ee031ea)
 Call ID: 6bfe147b-7d0a-4ba1-8f1e-49758ee031ea
  Args:
    type: :Woman
    source: Vittoria_dal_Pozzo
  AssignClass (857e20db-49e7-4609-90e6-ab3b1ca25976)
 Call ID: 857e20db-49e7-4609-90e6-ab3b1ca25976
  Args:
    type: :Person
    source: Vittoria_dal_Pozzo
  AddTriple (2bf3a574-d8ed-4238-98f3-cfa0e5023829)
 Call ID: 2bf3a574-d8ed-4238-98f3-cfa0e5023829
  Args:
    target: Vittoria_dal_Pozzo
    relation: :hasMother
    source: Prince_Emanuele_Filiberto
  AssignClass (3bdacfbd-0336-48d0-bd73-ef97197607f3)
 Call ID: 3bdacfbd-0336-48d0-bd73-ef97197607f3
  Args:
    type: :Man
    source: Philippe_comte_de_Paris
  AssignClass (9b1b0c6b-4a02-49b7-bab7-708b2863d3bf)
 Call ID: 9b1b0c6b-4a02-49b7-bab7-708b2863d3bf
  Args:
    type: :Person
    source: Philippe_comte_de_Paris
  AddTriple (d315ecf5-7ebb-46bc-9c96-f908deac4d52)
 Call ID: d315ecf5-7ebb-46bc-9c96-f908deac4d52
  Args:
    relation: :hasFather
    target: Philippe_comte_de_Paris
    source: Princess_Helene_of_Orleans
  AssignClass (cc87e3f9-e4dd-4a77-abd8-56241f152019)
 Call ID: cc87e3f9-e4dd-4a77-abd8-56241f152019
  Args:
    type: :Woman
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (19c50c42-643e-481c-97f7-a283bad3d9ff)
 Call ID: 19c50c42-643e-481c-97f7-a283bad3d9ff
  Args:
    type: :Person
    source: Princess_Marie_Isabelle_of_Orleans
  AddTriple (b9f584ee-c7e8-4f80-9f24-48739d231696)
 Call ID: b9f584ee-c7e8-4f80-9f24-48739d231696
  Args:
    relation: :hasMother
    target: Princess_Marie_Isabelle_of_Orleans
    source: Princess_Helene_of_Orleans
  AssignClass (751b1173-4123-4b61-8726-da84c9f60d06)
 Call ID: 751b1173-4123-4b61-8726-da84c9f60d06
  Args:
    type: :Man
    source: Prince_Luigi_Amedeo_Duke_of_the_Abruzzi
  AssignClass (975a2a77-bc7c-472e-9c27-9078e86adf67)
 Call ID: 975a2a77-bc7c-472e-9c27-9078e86adf67
  Args:
    type: :Person
    source: Prince_Luigi_Amedeo_Duke_of_the_Abruzzi
  AddTriple (2ab1edfc-413f-40e4-8901-4180150dbcc7)
 Call ID: 2ab1edfc-413f-40e4-8901-4180150dbcc7
  Args:
    source: Prince_Luigi_Amedeo_Duke_of_the_Abruzzi
    relation: :isUncleOf
    target: Prince_Aimone
  AssignClass (74d94150-7840-4da9-a8bd-a060e4fc54c0)
 Call ID: 74d94150-7840-4da9-a8bd-a060e4fc54c0
  Args:
    type: :Woman
    source: Princess_Irene_of_Greece_and_Denmark
  AssignClass (8cc4404f-ec90-43c2-945a-eb62ae41c4ce)
 Call ID: 8cc4404f-ec90-43c2-945a-eb62ae41c4ce
  Args:
    type: :Person
    source: Princess_Irene_of_Greece_and_Denmark
  AddLiteral (9a1401df-9f1e-482c-84c2-57b8bdcf86eb)
 Call ID: 9a1401df-9f1e-482c-84c2-57b8bdcf86eb
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1939
    source: Prince_Aimone
  AddTriple (831c50fc-5bf3-44ff-99d4-ffd2f4e9c3b4)
 Call ID: 831c50fc-5bf3-44ff-99d4-ffd2f4e9c3b4
  Args:
    target: Princess_Irene_of_Greece_and_Denmark
    relation: :hasRelation
    source: Prince_Aimone
  AssignClass (2aa1d7f8-d92e-4ba5-94ae-effa263b6fe3)
 Call ID: 2aa1d7f8-d92e-4ba5-94ae-effa263b6fe3
  Args:
    type: :Man
    source: King_Constantine_I
  AssignClass (a5d1ab4b-f750-4fb6-a596-247ccf047fe3)
 Call ID: a5d1ab4b-f750-4fb6-a596-247ccf047fe3
  Args:
    type: :Person
    source: King_Constantine_I
  AddTriple (038a5210-bbcd-478f-b005-cda862434773)
 Call ID: 038a5210-bbcd-478f-b005-cda862434773
  Args:
    source: Princess_Irene_of_Greece_and_Denmark
    relation: :hasFather
    target: King_Constantine_I
  AssignClass (d6941f88-8cad-497e-b0f4-45286275e9e7)
 Call ID: d6941f88-8cad-497e-b0f4-45286275e9e7
  Args:
    type: :Woman
    source: Princess_Sophie_of_Prussia
  AssignClass (ed5745c6-2941-4a97-9f67-fa7798e0da6b)
 Call ID: ed5745c6-2941-4a97-9f67-fa7798e0da6b
  Args:
    type: :Person
    source: Princess_Sophie_of_Prussia
  AddTriple (dcbdf6b8-2172-433e-a1e0-3f8a16026dc7)
 Call ID: dcbdf6b8-2172-433e-a1e0-3f8a16026dc7
  Args:
    relation: :hasMother
    target: Princess_Sophie_of_Prussia
    source: Princess_Irene_of_Greece_and_Denmark
  AssignClass (47067e66-6c2e-46fd-aaec-4868102ed4f7)
 Call ID: 47067e66-6c2e-46fd-aaec-4868102ed4f7
  Args:
    type: :Man
    source: Prince_Amedeo_Duke_of_Aosta_son
  AssignClass (f70cd045-6527-430a-b3d7-74d19a4e0c6e)
 Call ID: f70cd045-6527-430a-b3d7-74d19a4e0c6e
  Args:
    type: :Person
    source: Prince_Amedeo_Duke_of_Aosta_son
  AddTriple (71f10ecb-563f-4442-a0be-f6d0c1261dfb)
 Call ID: 71f10ecb-563f-4442-a0be-f6d0c1261dfb
  Args:
    relation: :hasSon
    target: Prince_Amedeo_Duke_of_Aosta_son
    source: Prince_Aimone
  AddTriple (268c6e22-5a77-4ca5-86ed-53d139b12bc4)
 Call ID: 268c6e22-5a77-4ca5-86ed-53d139b12bc4
  Args:
    target: Princess_Irene_of_Greece_and_Denmark
    relation: :hasMother
    source: Prince_Amedeo_Duke_of_Aosta_son
  Finish (b2597a60-5431-4704-a1ae-24d88e339a5a)
 Call ID: b2597a60-5431-4704-a1ae-24d88e339a5a
  Args: