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
Leopold IV, Prince of Lippe (Leopold Julius Bernhard Adalbert Otto Karl Gustav; 30 May 1871 – 30 December 1949) was the final sovereign of the Principality of Lippe in northwestern Germany from 1905 until his abdication in 1918.
He was the first and only ruler of Lippe of the Lippe-Biesterfeld branch.
Early life

He was born as Count Leopold of Lippe-Biesterfeld in Oberkassel, the son of Ernest, Count of Lippe-Biesterfeld and Countess Karoline of Wartensleben.
Leopold belonged to the Lippe-Biesterfeld line of the House of Lippe which was the most senior line of the princely house after the reigning Lippe-Detmold line.
Ruler of Lippe

Since 1895, the Principality of Lippe had been ruled by a regent due to the incapacity of Prince Alexander.
Leopold's father had acted as regent since 1897, and following his death on 26 September 1904, Leopold assumed the regency.
This was not recognized by the German Emperor Wilhelm II, who initially refused to legally recognize Leopold as regent as there was an issue over whether Leopold and his siblings were of legitimate rank, and as such eligible for the succession.
As a result, the Diet of Lippe appointed a high commission to consider the matter.
The regency issue was still ongoing when Prince Alexander died on 13 January 1905.
Leopold was confirmed as Prince of Lippe and Alexander's successor on 25 October 1905, following a court ruling.
On 3 June 1911, while out motoring, Leopold and his brother Prince Julius were attacked by a gang of Italian laborers who hurled a shower of missiles at the princes.
Though Leopold escaped unhurt, his brother received a head wound.
During World War I, Leopold upgraded the titles of the various lines of the House of Lippe.
One of the members to benefit from the granting of titles was Leopold's nephew Count Bernhard of Biesterfeld (son of Leopold's brother Bernhard), who would go on to become the Prince Consort of Queen Juliana of the Netherlands.
On 24 February 1916, Bernhard and his brother were upgraded to the title Prince of Lippe-Biesterfeld with the style Serene Highness.
The Counts of Lippe-Weissenfeld also benefited with creations of the title Prince of Lippe-Weissenfeld, with the style Serene Highness, taking place on 24 February 1916 for Count Clemens and his descendants, and again on 9 November 1918 for the other members of this line.
Just three days after upgrading the titles of members of the Lippe-Weissenfeld line, and following the German Empire's defeat in World War I and the subsequent revolution, Leopold was forced to renounce the throne on 12 November 1918.
Following the end of his rule, the Principality of Lippe was transformed into a Free state in the new Weimar Republic.
His eldest son the Hereditary Prince Ernst is reported to have been the first German prince to join the party when he signed up in May 1928.
In addition to being pro Nazi, both Hereditary Prince Ernst and Prince Chlodwig had contracted unequal marriages.
So in 1947 when Leopold wrote his will, Armin, his youngest son and only child with his second wife, would succeed him as head of the House of Lippe and also become administrator of the princely family's properties such as Schloss Detmold.
Thus when Leopold died in Detmold his three eldest sons were all disinherited and his youngest son Armin became head of the princely house.
Marriages and children

Leopold was married to Princess Bertha of Hesse-Philippsthal-Barchfeld (1874–1919) on 16 August 1901 in Rotenburg.



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
  AssignClass (bc03d870-313f-4890-9b10-5f9db462e286)
 Call ID: bc03d870-313f-4890-9b10-5f9db462e286
  Args:
    type: :Man
    source: Leopold_IV
  AssignClass (83bc8953-1a14-4c12-a407-36d89322d9dc)
 Call ID: 83bc8953-1a14-4c12-a407-36d89322d9dc
  Args:
    type: :Person
    source: Leopold_IV
  AddLiteral (28a50771-3565-4d11-82d9-68db45e6fc08)
 Call ID: 28a50771-3565-4d11-82d9-68db45e6fc08
  Args:
    source: Leopold_IV
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1871
  AddLiteral (6c21ae4a-4598-4a1d-9b05-7643fb030dcc)
 Call ID: 6c21ae4a-4598-4a1d-9b05-7643fb030dcc
  Args:
    literal_value: 1949
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Leopold_IV
  AssignClass (df4efc84-6827-4cbc-919e-ef75f81f51f0)
 Call ID: df4efc84-6827-4cbc-919e-ef75f81f51f0
  Args:
    source: Ernest_Count_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (8985fcef-bfd7-4168-995b-919778189fe8)
 Call ID: 8985fcef-bfd7-4168-995b-919778189fe8
  Args:
    type: :Person
    source: Ernest_Count_of_Lippe-Biesterfeld
  AssignClass (bb4e09d1-320f-4c33-b131-cd7f8a2eece2)
 Call ID: bb4e09d1-320f-4c33-b131-cd7f8a2eece2
  Args:
    type: :Woman
    source: Karoline_of_Wartensleben
  AssignClass (5e8739cd-0342-46d4-b2df-76827a2b3447)
 Call ID: 5e8739cd-0342-46d4-b2df-76827a2b3447
  Args:
    type: :Person
    source: Karoline_of_Wartensleben
  AddTriple (34d445f6-006c-4235-b8d5-d34ece104e4d)
 Call ID: 34d445f6-006c-4235-b8d5-d34ece104e4d
  Args:
    source: Leopold_IV
    target: Ernest_Count_of_Lippe-Biesterfeld
    relation: :hasFather
  AddTriple (63c7bf39-283b-442a-97b2-5c626c10b363)
 Call ID: 63c7bf39-283b-442a-97b2-5c626c10b363
  Args:
    relation: :hasMother
    target: Karoline_of_Wartensleben
    source: Leopold_IV
  AssignClass (16e096c1-f5b4-4045-9da7-fecadf1b6c89)
 Call ID: 16e096c1-f5b4-4045-9da7-fecadf1b6c89
  Args:
    source: Prince_Julius
    type: :Man
  AssignClass (e3823070-eae1-4118-baa1-e71e62a9750a)
 Call ID: e3823070-eae1-4118-baa1-e71e62a9750a
  Args:
    source: Prince_Julius
    type: :Person
  AddTriple (89edab36-51d9-425a-93bf-589c756bd850)
 Call ID: 89edab36-51d9-425a-93bf-589c756bd850
  Args:
    target: Leopold_IV
    relation: :isBrotherOf
    source: Prince_Julius
  AssignClass (0145c168-de07-4b8d-a20c-397b62b1e334)
 Call ID: 0145c168-de07-4b8d-a20c-397b62b1e334
  Args:
    source: Bernhard_of_Biesterfeld_nephew
    type: :Man
  AssignClass (cc67e82a-9a57-498f-8489-f984324fb8c4)
 Call ID: cc67e82a-9a57-498f-8489-f984324fb8c4
  Args:
    source: Bernhard_of_Biesterfeld_nephew
    type: :Person
  AssignClass (d0d92fe0-330c-4a8b-8d15-a3eb6d0845cb)
 Call ID: d0d92fe0-330c-4a8b-8d15-a3eb6d0845cb
  Args:
    type: :Man
    source: Bernhard_of_Biesterfeld_father
  AssignClass (54dab89f-7105-4586-ab97-53158cd898ab)
 Call ID: 54dab89f-7105-4586-ab97-53158cd898ab
  Args:
    type: :Person
    source: Bernhard_of_Biesterfeld_father
  AddTriple (780bb4bc-f01e-4c70-aa78-dccf8952b6e9)
 Call ID: 780bb4bc-f01e-4c70-aa78-dccf8952b6e9
  Args:
    source: Bernhard_of_Biesterfeld_nephew
    relation: :hasFather
    target: Bernhard_of_Biesterfeld_father
  AddTriple (da0a4d2b-5174-4d50-87de-91613a3e034a)
 Call ID: da0a4d2b-5174-4d50-87de-91613a3e034a
  Args:
    target: Leopold_IV
    relation: :isBrotherOf
    source: Bernhard_of_Biesterfeld_father
  AssignClass (781961fe-fd6c-4dbf-b9ea-5a42e64dd619)
 Call ID: 781961fe-fd6c-4dbf-b9ea-5a42e64dd619
  Args:
    type: :Man
    source: Hereditary_Prince_Ernst
  AssignClass (5a760751-d3d6-4924-9574-57b800762bb4)
 Call ID: 5a760751-d3d6-4924-9574-57b800762bb4
  Args:
    source: Hereditary_Prince_Ernst
    type: :Person
  AddTriple (4809b154-2531-49f8-bd8c-6cb39050b5bf)
 Call ID: 4809b154-2531-49f8-bd8c-6cb39050b5bf
  Args:
    source: Hereditary_Prince_Ernst
    target: Leopold_IV
    relation: :hasFather
  AssignClass (4695343c-4622-43c0-9522-c29a9590a476)
 Call ID: 4695343c-4622-43c0-9522-c29a9590a476
  Args:
    type: :Man
    source: Prince_Chlodwig
  AssignClass (20741506-dd84-43b1-934a-f84fc8687ab4)
 Call ID: 20741506-dd84-43b1-934a-f84fc8687ab4
  Args:
    type: :Person
    source: Prince_Chlodwig
  AddTriple (c5576226-81d1-4e99-be21-dc3bb34392db)
 Call ID: c5576226-81d1-4e99-be21-dc3bb34392db
  Args:
    relation: :hasFather
    target: Leopold_IV
    source: Prince_Chlodwig
  AssignClass (f33fca7d-7e66-4a42-870c-5b76a4feaa06)
 Call ID: f33fca7d-7e66-4a42-870c-5b76a4feaa06
  Args:
    source: Armin
    type: :Man
  AssignClass (09f7a704-0686-489d-b9f5-07afff55b2e3)
 Call ID: 09f7a704-0686-489d-b9f5-07afff55b2e3
  Args:
    type: :Person
    source: Armin
  AddTriple (e83f2a7b-6033-4cb4-9673-e44d99535ba2)
 Call ID: e83f2a7b-6033-4cb4-9673-e44d99535ba2
  Args:
    source: Armin
    target: Leopold_IV
    relation: :hasFather
  AssignClass (09d3830d-8cee-47ba-9572-187de49a4ec2)
 Call ID: 09d3830d-8cee-47ba-9572-187de49a4ec2
  Args:
    type: :Woman
    source: Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
  AssignClass (3da648e1-07f9-4c24-b57a-66e3d1bbda80)
 Call ID: 3da648e1-07f9-4c24-b57a-66e3d1bbda80
  Args:
    type: :Person
    source: Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
  AddLiteral (aa4ba800-e272-4251-84b5-ed99d336b3bc)
 Call ID: aa4ba800-e272-4251-84b5-ed99d336b3bc
  Args:
    literal_value: 1874
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
  AddLiteral (8a0a14f3-e931-4343-9fe8-383ba032acaf)
 Call ID: 8a0a14f3-e931-4343-9fe8-383ba032acaf
  Args:
    source: Princess_Bertha_of_Hesse-Philippsthal-Barchfeld
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1919
  AddLiteral (eff51052-0364-47b2-be8d-827babab0447)
 Call ID: eff51052-0364-47b2-be8d-827babab0447
  Args:
    relation: :hasMarriageYear
    literal_value: 1901
    literal_type: xsd:integer
    source: Leopold_IV
  AddTriple (567e2d89-4cb2-4e08-aa76-e2e04557c73e)
 Call ID: 567e2d89-4cb2-4e08-aa76-e2e04557c73e
  Args:
    relation: :hasMother
    target: Second_Wife_of_Leopold_IV
    source: Armin
  AssignClass (99e31a0e-a693-4126-9172-348c1a60af66)
 Call ID: 99e31a0e-a693-4126-9172-348c1a60af66
  Args:
    type: :Woman
    source: Second_Wife_of_Leopold_IV
  AssignClass (657ff49a-ffcd-4179-bb88-8bc14bc09334)
 Call ID: 657ff49a-ffcd-4179-bb88-8bc14bc09334
  Args:
    type: :Person
    source: Second_Wife_of_Leopold_IV
  Finish (20ecdc22-f10d-4fdc-ad08-ca04c4e06c6f)
 Call ID: 20ecdc22-f10d-4fdc-ad08-ca04c4e06c6f
  Args: