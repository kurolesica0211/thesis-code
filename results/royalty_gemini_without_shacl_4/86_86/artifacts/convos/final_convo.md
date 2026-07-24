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
  AssignClass (a15e416f-248f-47c4-9aaf-ce45e7b8ab1c)
 Call ID: a15e416f-248f-47c4-9aaf-ce45e7b8ab1c
  Args:
    source: Aimone_Duke_of_Aosta
    type: :Man
  AssignClass (56f76817-147f-4d9d-ac3c-d6b316ef4daf)
 Call ID: 56f76817-147f-4d9d-ac3c-d6b316ef4daf
  Args:
    type: :Person
    source: Aimone_Duke_of_Aosta
  AddLiteral (549a8289-2201-4a03-bf9c-3e96cff740d5)
 Call ID: 549a8289-2201-4a03-bf9c-3e96cff740d5
  Args:
    literal_value: 1900
    relation: :hasBirthYear
    source: Aimone_Duke_of_Aosta
    literal_type: xsd:integer
  AddLiteral (780bf16a-0003-48c2-917c-f2e162b38f7c)
 Call ID: 780bf16a-0003-48c2-917c-f2e162b38f7c
  Args:
    relation: :hasDeathYear
    source: Aimone_Duke_of_Aosta
    literal_value: 1948
    literal_type: xsd:integer
  AssignClass (7dd41fa7-25d1-4d3d-a7a2-82c453328e8d)
 Call ID: 7dd41fa7-25d1-4d3d-a7a2-82c453328e8d
  Args:
    type: :Man
    source: Emanuele_Filiberto_Duke_of_Aosta
  AssignClass (4cf2bb7b-8000-4b80-9f36-c407d122e163)
 Call ID: 4cf2bb7b-8000-4b80-9f36-c407d122e163
  Args:
    source: Emanuele_Filiberto_Duke_of_Aosta
    type: :Person
  AddTriple (9cf08956-3b43-4af6-a556-1e3ac07660bb)
 Call ID: 9cf08956-3b43-4af6-a556-1e3ac07660bb
  Args:
    source: Aimone_Duke_of_Aosta
    relation: :isSonOf
    target: Emanuele_Filiberto_Duke_of_Aosta
  AssignClass (5c8c1153-b850-4214-b285-56e0f7e618bf)
 Call ID: 5c8c1153-b850-4214-b285-56e0f7e618bf
  Args:
    source: Amedeo_3rd_Duke_of_Aosta
    type: :Man
  AssignClass (b233e17c-2f0b-49f6-97ef-c77eaf3bc8cd)
 Call ID: b233e17c-2f0b-49f6-97ef-c77eaf3bc8cd
  Args:
    type: :Person
    source: Amedeo_3rd_Duke_of_Aosta
  AddTriple (de38ae36-069a-4839-a3f9-48c327a72b27)
 Call ID: de38ae36-069a-4839-a3f9-48c327a72b27
  Args:
    source: Aimone_Duke_of_Aosta
    relation: :isBrotherOf
    target: Amedeo_3rd_Duke_of_Aosta
  AssignClass (eb16e778-a252-49a1-b5fc-378b238c70d5)
 Call ID: eb16e778-a252-49a1-b5fc-378b238c70d5
  Args:
    source: Princess_Helene_of_Orleans
    type: :Woman
  AssignClass (6d753d23-74e5-46e7-8fd1-c5b1b421e9a2)
 Call ID: 6d753d23-74e5-46e7-8fd1-c5b1b421e9a2
  Args:
    type: :Person
    source: Princess_Helene_of_Orleans
  AddTriple (1188ee39-c752-43a9-9f29-88b7b43db70b)
 Call ID: 1188ee39-c752-43a9-9f29-88b7b43db70b
  Args:
    relation: :hasMother
    source: Aimone_Duke_of_Aosta
    target: Princess_Helene_of_Orleans
  AssignClass (e3a86da2-9145-4b11-bad0-d00a7d9afe4a)
 Call ID: e3a86da2-9145-4b11-bad0-d00a7d9afe4a
  Args:
    source: Prince_Amedeo_1st_Duke_of_Aosta
    type: :Man
  AssignClass (23bb3984-f963-4a29-89b1-90d35478afc3)
 Call ID: 23bb3984-f963-4a29-89b1-90d35478afc3
  Args:
    source: Prince_Amedeo_1st_Duke_of_Aosta
    type: :Person
  AddTriple (14198415-f45b-4bc4-8d2a-b8e9231b3684)
 Call ID: 14198415-f45b-4bc4-8d2a-b8e9231b3684
  Args:
    relation: :isFatherOf
    source: Prince_Amedeo_1st_Duke_of_Aosta
    target: Emanuele_Filiberto_Duke_of_Aosta
  AssignClass (fc1a69a2-d762-40dc-972b-1766d847c51a)
 Call ID: fc1a69a2-d762-40dc-972b-1766d847c51a
  Args:
    type: :Woman
    source: Vittoria_dal_Pozzo_Principessa_della_Cisterna
  AssignClass (16dff978-6ec4-4b40-8c39-c9fae0ddf9b8)
 Call ID: 16dff978-6ec4-4b40-8c39-c9fae0ddf9b8
  Args:
    type: :Person
    source: Vittoria_dal_Pozzo_Principessa_della_Cisterna
  AddTriple (ac644a8d-f8e9-4842-9446-46d8f3d4f984)
 Call ID: ac644a8d-f8e9-4842-9446-46d8f3d4f984
  Args:
    target: Emanuele_Filiberto_Duke_of_Aosta
    relation: :isMotherOf
    source: Vittoria_dal_Pozzo_Principessa_della_Cisterna
  AssignClass (7a862c09-2355-49b7-a626-543e76fe4658)
 Call ID: 7a862c09-2355-49b7-a626-543e76fe4658
  Args:
    source: Philippe_Comte_de_Paris
    type: :Man
  AssignClass (b5fc5da8-7a17-4e30-a4d7-edee658d5ad8)
 Call ID: b5fc5da8-7a17-4e30-a4d7-edee658d5ad8
  Args:
    type: :Person
    source: Philippe_Comte_de_Paris
  AssignClass (3a384f41-68dc-4efa-8068-48014f3d0c5f)
 Call ID: 3a384f41-68dc-4efa-8068-48014f3d0c5f
  Args:
    type: :Woman
    source: Princess_Marie_Isabelle_of_Orleans
  AssignClass (05919172-71b1-48b8-8a85-859ba78cf322)
 Call ID: 05919172-71b1-48b8-8a85-859ba78cf322
  Args:
    source: Princess_Marie_Isabelle_of_Orleans
    type: :Person
  AddTriple (25c7ee98-7f0f-4642-8a1c-1d86703085d2)
 Call ID: 25c7ee98-7f0f-4642-8a1c-1d86703085d2
  Args:
    target: Princess_Helene_of_Orleans
    source: Philippe_Comte_de_Paris
    relation: :isFatherOf
  AddTriple (3f59d80d-6763-4316-a63a-a3ea502f11ad)
 Call ID: 3f59d80d-6763-4316-a63a-a3ea502f11ad
  Args:
    target: Princess_Helene_of_Orleans
    source: Princess_Marie_Isabelle_of_Orleans
    relation: :isMotherOf
  AssignClass (3d8e86d7-0be7-4a4c-9111-b0b58e1ea614)
 Call ID: 3d8e86d7-0be7-4a4c-9111-b0b58e1ea614
  Args:
    type: :Man
    source: Prince_Luigi_Amedeo_Duke_of_the_Abruzzi
  AssignClass (b4616fd7-f364-4335-bb8f-6c9864d7ec59)
 Call ID: b4616fd7-f364-4335-bb8f-6c9864d7ec59
  Args:
    source: Prince_Luigi_Amedeo_Duke_of_the_Abruzzi
    type: :Person
  AssignClass (d11b854e-c6fe-4328-8694-c3a90756f3a4)
 Call ID: d11b854e-c6fe-4328-8694-c3a90756f3a4
  Args:
    source: Princess_Irene_of_Greece_and_Denmark
    type: :Woman
  AssignClass (d9f900c6-8b2b-42e5-b462-7b12cd08c06e)
 Call ID: d9f900c6-8b2b-42e5-b462-7b12cd08c06e
  Args:
    type: :Person
    source: Princess_Irene_of_Greece_and_Denmark
  AddLiteral (b72e898a-07fb-4f0a-8e76-014669c1d53e)
 Call ID: b72e898a-07fb-4f0a-8e76-014669c1d53e
  Args:
    literal_value: 1939
    relation: :hasMarriageYear
    source: Aimone_Duke_of_Aosta
    literal_type: xsd:integer
  AddTriple (2805108c-ab3a-466c-a5f8-142c842ffbe2)
 Call ID: 2805108c-ab3a-466c-a5f8-142c842ffbe2
  Args:
    source: Aimone_Duke_of_Aosta
    relation: :hasRelation
    target: Princess_Irene_of_Greece_and_Denmark
  AssignClass (c453422b-f7ca-490c-b087-47f29f13c1ed)
 Call ID: c453422b-f7ca-490c-b087-47f29f13c1ed
  Args:
    source: King_Constantine_I
    type: :Man
  AssignClass (ca6fbce3-5388-4367-9f84-8b0d779ee1da)
 Call ID: ca6fbce3-5388-4367-9f84-8b0d779ee1da
  Args:
    source: King_Constantine_I
    type: :Person
  AssignClass (3f70692b-8783-4ec2-993f-1655127a85f1)
 Call ID: 3f70692b-8783-4ec2-993f-1655127a85f1
  Args:
    source: Princess_Sophie_of_Prussia
    type: :Woman
  AssignClass (ce6f3efe-26fa-4607-a183-8c786a54bc2a)
 Call ID: ce6f3efe-26fa-4607-a183-8c786a54bc2a
  Args:
    type: :Person
    source: Princess_Sophie_of_Prussia
  AddTriple (7059ef76-5171-4f1c-adf8-a5199dcc4e50)
 Call ID: 7059ef76-5171-4f1c-adf8-a5199dcc4e50
  Args:
    relation: :isFatherOf
    source: King_Constantine_I
    target: Princess_Irene_of_Greece_and_Denmark
  AddTriple (42d8f73f-101d-4ba8-83d4-ad74cb23914b)
 Call ID: 42d8f73f-101d-4ba8-83d4-ad74cb23914b
  Args:
    target: Princess_Irene_of_Greece_and_Denmark
    relation: :isMotherOf
    source: Princess_Sophie_of_Prussia
  AssignClass (365de6df-4f9c-431b-bb78-4d2e48a8fa92)
 Call ID: 365de6df-4f9c-431b-bb78-4d2e48a8fa92
  Args:
    source: Prince_Amedeo_Duke_of_Aosta_1943
    type: :Man
  AssignClass (d63c5a64-0362-4be6-b221-b24ad46cb02e)
 Call ID: d63c5a64-0362-4be6-b221-b24ad46cb02e
  Args:
    type: :Person
    source: Prince_Amedeo_Duke_of_Aosta_1943
  AddTriple (ef6f5608-fadf-422a-bbbd-2cd86722cda2)
 Call ID: ef6f5608-fadf-422a-bbbd-2cd86722cda2
  Args:
    target: Aimone_Duke_of_Aosta
    relation: :isSonOf
    source: Prince_Amedeo_Duke_of_Aosta_1943
  AddTriple (7692e01b-4c0d-411a-b193-b1b606aeee74)
 Call ID: 7692e01b-4c0d-411a-b193-b1b606aeee74
  Args:
    source: Prince_Amedeo_Duke_of_Aosta_1943
    relation: :isSonOf
    target: Princess_Irene_of_Greece_and_Denmark
  Finish (f01ddc9e-c44c-47c4-a75a-bd0a14372206)
 Call ID: f01ddc9e-c44c-47c4-a75a-bd0a14372206
  Args: