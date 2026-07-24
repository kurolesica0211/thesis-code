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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



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
  AssignClass (7fa3c50e-2d70-4780-9255-32c39c6450c8)
 Call ID: 7fa3c50e-2d70-4780-9255-32c39c6450c8
  Args:
    type: :Man
    source: :Henri_Philippe_Pierre_Marie_d_Orleans
  AssignClass (5e8c1a08-e7a0-4fde-8003-0a7a02a434bf)
 Call ID: 5e8c1a08-e7a0-4fde-8003-0a7a02a434bf
  Args:
    source: :Henri_Philippe_Pierre_Marie_d_Orleans
    type: :Person
  AddLiteral (7a94e442-a538-48c6-9f90-c8ebc391f086)
 Call ID: 7a94e442-a538-48c6-9f90-c8ebc391f086
  Args:
    literal_type: xsd:integer
    literal_value: 1933
    relation: :hasBirthYear
    source: :Henri_Philippe_Pierre_Marie_d_Orleans
  AddLiteral (c711519c-83fe-486b-9629-08e50914071b)
 Call ID: c711519c-83fe-486b-9629-08e50914071b
  Args:
    relation: :hasDeathYear
    source: :Henri_Philippe_Pierre_Marie_d_Orleans
    literal_value: 2019
    literal_type: xsd:integer
  AssignClass (d4e828de-829e-49eb-9263-6613f94fab14)
 Call ID: d4e828de-829e-49eb-9263-6613f94fab14
  Args:
    type: :Man
    source: :Henri_Count_of_Paris
  AssignClass (c40bca1f-a34f-4e34-b917-1c14dc301857)
 Call ID: c40bca1f-a34f-4e34-b917-1c14dc301857
  Args:
    type: :Person
    source: :Henri_Count_of_Paris
  AddLiteral (27c37010-441c-4474-a77f-bcd2fbf908b3)
 Call ID: 27c37010-441c-4474-a77f-bcd2fbf908b3
  Args:
    literal_type: xsd:integer
    literal_value: 1908
    source: :Henri_Count_of_Paris
    relation: :hasBirthYear
  AddLiteral (0b5b2bca-d00a-4a57-bd8f-26049264b130)
 Call ID: 0b5b2bca-d00a-4a57-bd8f-26049264b130
  Args:
    literal_type: xsd:integer
    source: :Henri_Count_of_Paris
    relation: :hasDeathYear
    literal_value: 1999
  AddTriple (6d9ef967-fcec-4110-99c1-d1a7710e62a3)
 Call ID: 6d9ef967-fcec-4110-99c1-d1a7710e62a3
  Args:
    source: :Henri_Philippe_Pierre_Marie_d_Orleans
    target: :Henri_Count_of_Paris
    relation: :hasFather
  AssignClass (4a183c53-f586-4bcf-ac05-39e4946559f2)
 Call ID: 4a183c53-f586-4bcf-ac05-39e4946559f2
  Args:
    source: :Princess_Isabelle_of_Orleans_Braganza
    type: :Woman
  AssignClass (4f1862f6-9465-4561-831f-2fb3a75c3b8a)
 Call ID: 4f1862f6-9465-4561-831f-2fb3a75c3b8a
  Args:
    source: :Princess_Isabelle_of_Orleans_Braganza
    type: :Person
  AddTriple (855b46ea-e70a-4100-966a-7b0364fa5343)
 Call ID: 855b46ea-e70a-4100-966a-7b0364fa5343
  Args:
    relation: :hasMother
    target: :Princess_Isabelle_of_Orleans_Braganza
    source: :Henri_Philippe_Pierre_Marie_d_Orleans
  AddTriple (f55f9c5d-dd1a-41a4-9eb6-92c364fc6ad5)
 Call ID: f55f9c5d-dd1a-41a4-9eb6-92c364fc6ad5
  Args:
    target: :Henri_Count_of_Paris
    source: :Princess_Isabelle_of_Orleans_Braganza
    relation: :hasFather
  AssignClass (068bb42e-16ec-4aaf-8284-de8dc341794b)
 Call ID: 068bb42e-16ec-4aaf-8284-de8dc341794b
  Args:
    source: :Francois_d_Orleans
    type: :Man
  AssignClass (8699d273-24ea-4af1-9649-e26805d01e99)
 Call ID: 8699d273-24ea-4af1-9649-e26805d01e99
  Args:
    source: :Francois_d_Orleans
    type: :Person
  AddTriple (72200bc6-61dc-4f9c-9a90-119460e8b128)
 Call ID: 72200bc6-61dc-4f9c-9a90-119460e8b128
  Args:
    relation: :isSiblingOf
    target: :Francois_d_Orleans
    source: :Henri_Philippe_Pierre_Marie_d_Orleans
  AssignClass (6b9c7753-a18f-466b-859a-e56df6a0281b)
 Call ID: 6b9c7753-a18f-466b-859a-e56df6a0281b
  Args:
    source: :Duchess_Marie_Therese_of_Wurttemberg
    type: :Woman
  AssignClass (7f51ffec-c6d1-4065-b2bd-984e5301c142)
 Call ID: 7f51ffec-c6d1-4065-b2bd-984e5301c142
  Args:
    type: :Person
    source: :Duchess_Marie_Therese_of_Wurttemberg
  AddLiteral (a287b0cf-150c-441f-9c7a-9e76968adc0b)
 Call ID: a287b0cf-150c-441f-9c7a-9e76968adc0b
  Args:
    source: :Duchess_Marie_Therese_of_Wurttemberg
    relation: :hasBirthYear
    literal_value: 1934
    literal_type: xsd:integer
  AddLiteral (c2944086-99f8-422e-a81b-c0c1e794d94e)
 Call ID: c2944086-99f8-422e-a81b-c0c1e794d94e
  Args:
    literal_value: 1984
    relation: :hasMarriageYear
    source: :Henri_Philippe_Pierre_Marie_d_Orleans
    literal_type: xsd:integer
  AssignClass (4c6be25a-18a9-41a8-aba0-e76cc4117b43)
 Call ID: 4c6be25a-18a9-41a8-aba0-e76cc4117b43
  Args:
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    type: :Woman
  AssignClass (9a9356d8-62c1-407d-add6-5aa24723b4d3)
 Call ID: 9a9356d8-62c1-407d-add6-5aa24723b4d3
  Args:
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    type: :Person
  AddLiteral (4ae49b67-064d-41c6-a9c0-e586ba2f2ded)
 Call ID: 4ae49b67-064d-41c6-a9c0-e586ba2f2ded
  Args:
    relation: :hasBirthYear
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_value: 1938
    literal_type: xsd:integer
  AddLiteral (bfe8155b-00fd-46b4-93b1-63fdbae29503)
 Call ID: bfe8155b-00fd-46b4-93b1-63fdbae29503
  Args:
    relation: :hasDeathYear
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    literal_value: 2022
    literal_type: xsd:integer
  AddLiteral (eae5fa0b-c407-447e-94e9-206fdfcf89e2)
 Call ID: eae5fa0b-c407-447e-94e9-206fdfcf89e2
  Args:
    literal_value: 1984
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (61fa7efd-527f-42d9-9cde-ef2a1ff8e826)
 Call ID: 61fa7efd-527f-42d9-9cde-ef2a1ff8e826
  Args:
    type: :Man
    source: :Luis_Cousino_y_Sebire
  AssignClass (7be16929-6f72-4789-8367-ff37f4970584)
 Call ID: 7be16929-6f72-4789-8367-ff37f4970584
  Args:
    source: :Luis_Cousino_y_Sebire
    type: :Person
  AssignClass (5fa93d15-9dc5-45be-b5df-e5566048eaa6)
 Call ID: 5fa93d15-9dc5-45be-b5df-e5566048eaa6
  Args:
    source: :Antonia_Maria_Quinones_de_Leon_y_Banuelos
    type: :Woman
  AssignClass (38758341-61be-48a5-bbc3-30f5864c5641)
 Call ID: 38758341-61be-48a5-bbc3-30f5864c5641
  Args:
    source: :Antonia_Maria_Quinones_de_Leon_y_Banuelos
    type: :Person
  AddTriple (1dac97fa-611a-444a-80e4-1ac860fb3df7)
 Call ID: 1dac97fa-611a-444a-80e4-1ac860fb3df7
  Args:
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    target: :Luis_Cousino_y_Sebire
    relation: :hasFather
  AddTriple (1c67dfc3-003b-4f14-927c-6d749d5cc1e1)
 Call ID: 1c67dfc3-003b-4f14-927c-6d749d5cc1e1
  Args:
    relation: :hasMother
    source: :Micaela_Anna_Maria_Cousino_y_Quinones_de_Leon
    target: :Antonia_Maria_Quinones_de_Leon_y_Banuelos
  AssignClass (c956f1f3-436f-4a0d-933c-1c64abee7420)
 Call ID: c956f1f3-436f-4a0d-933c-1c64abee7420
  Args:
    type: :Woman
    source: :Marie_d_Orleans
  AssignClass (1635006a-1916-4d42-99ec-83f90f04e3d3)
 Call ID: 1635006a-1916-4d42-99ec-83f90f04e3d3
  Args:
    source: :Marie_d_Orleans
    type: :Person
  AddTriple (881b0121-0354-489d-aed5-af469b1f44ce)
 Call ID: 881b0121-0354-489d-aed5-af469b1f44ce
  Args:
    relation: :isDaughterOf
    target: :Henri_Philippe_Pierre_Marie_d_Orleans
    source: :Marie_d_Orleans
  AddTriple (71adc3b4-d39d-4ba6-b58f-d0d656ba99c4)
 Call ID: 71adc3b4-d39d-4ba6-b58f-d0d656ba99c4
  Args:
    target: :Duchess_Marie_Therese_of_Wurttemberg
    source: :Marie_d_Orleans
    relation: :isDaughterOf
  AssignClass (cb2627dc-6968-4c31-88a8-63619b383ab7)
 Call ID: cb2627dc-6968-4c31-88a8-63619b383ab7
  Args:
    type: :Man
    source: :Prince_Gundakar_of_Liechtenstein
  AssignClass (c406059e-8608-4e9a-b82d-81bd45a40f72)
 Call ID: c406059e-8608-4e9a-b82d-81bd45a40f72
  Args:
    source: :Prince_Gundakar_of_Liechtenstein
    type: :Person
  AssignClass (b7de79a5-06e8-45b1-9743-80ecb064e91d)
 Call ID: b7de79a5-06e8-45b1-9743-80ecb064e91d
  Args:
    source: :Diane_d_Orleans
    type: :Woman
  AssignClass (6ab4f7d1-c44a-41c0-a7e0-a99fbc8810ec)
 Call ID: 6ab4f7d1-c44a-41c0-a7e0-a99fbc8810ec
  Args:
    source: :Diane_d_Orleans
    type: :Person
  AddTriple (32742f81-3728-450f-94d3-f24b53758f3b)
 Call ID: 32742f81-3728-450f-94d3-f24b53758f3b
  Args:
    source: :Diane_d_Orleans
    target: :Henri_Philippe_Pierre_Marie_d_Orleans
    relation: :isSisterOf
  AssignClass (348ea4ac-4684-440b-a3a7-01deca8ebc04)
 Call ID: 348ea4ac-4684-440b-a3a7-01deca8ebc04
  Args:
    source: :Michel_d_Orleans
    type: :Man
  AssignClass (6a45ed41-b53b-46b5-8a88-9c38c8fc3176)
 Call ID: 6a45ed41-b53b-46b5-8a88-9c38c8fc3176
  Args:
    type: :Person
    source: :Michel_d_Orleans
  AddTriple (ae83bc0a-25fc-4feb-8f72-6314e6da7a88)
 Call ID: ae83bc0a-25fc-4feb-8f72-6314e6da7a88
  Args:
    source: :Michel_d_Orleans
    target: :Henri_Philippe_Pierre_Marie_d_Orleans
    relation: :isBrotherOf
  AssignClass (db1dd702-52f1-4a53-8f00-c63dcc2d9c77)
 Call ID: db1dd702-52f1-4a53-8f00-c63dcc2d9c77
  Args:
    type: :Man
    source: :Thibaut_d_Orleans
  AssignClass (63c45ece-65a8-4644-b5bb-a79e3df65657)
 Call ID: 63c45ece-65a8-4644-b5bb-a79e3df65657
  Args:
    type: :Person
    source: :Thibaut_d_Orleans
  AddTriple (749b021c-adb9-4814-bb0d-0471b182dc82)
 Call ID: 749b021c-adb9-4814-bb0d-0471b182dc82
  Args:
    source: :Thibaut_d_Orleans
    target: :Henri_Philippe_Pierre_Marie_d_Orleans
    relation: :isBrotherOf
  AssignClass (29046f27-4c37-4721-b197-6b3e0803421d)
 Call ID: 29046f27-4c37-4721-b197-6b3e0803421d
  Args:
    source: :Jacques_d_Orleans
    type: :Man
  AssignClass (5d18f45a-ee18-4c52-8ee5-d954a4ee9454)
 Call ID: 5d18f45a-ee18-4c52-8ee5-d954a4ee9454
  Args:
    source: :Jacques_d_Orleans
    type: :Person
  AddTriple (d93b9848-d600-46b0-ae72-eb41d1b9f5bb)
 Call ID: d93b9848-d600-46b0-ae72-eb41d1b9f5bb
  Args:
    relation: :isBrotherOf
    target: :Henri_Philippe_Pierre_Marie_d_Orleans
    source: :Jacques_d_Orleans
  AssignClass (931ac598-098d-4eb8-bbcc-fb3100ae3b61)
 Call ID: 931ac598-098d-4eb8-bbcc-fb3100ae3b61
  Args:
    type: :Man
    source: :Charles_Louis_d_Orleans
  AssignClass (46cdb376-b319-400c-a772-71dd0bed7aea)
 Call ID: 46cdb376-b319-400c-a772-71dd0bed7aea
  Args:
    source: :Charles_Louis_d_Orleans
    type: :Person
  AddLiteral (703633b1-9d0b-4523-9698-75ecf02e65c1)
 Call ID: 703633b1-9d0b-4523-9698-75ecf02e65c1
  Args:
    literal_value: 1972
    source: :Charles_Louis_d_Orleans
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (36df11cf-631a-48d2-b8e9-ab731da59bd4)
 Call ID: 36df11cf-631a-48d2-b8e9-ab731da59bd4
  Args:
    relation: :isSonOf
    target: :Jacques_d_Orleans
    source: :Charles_Louis_d_Orleans
  AssignClass (5e8bbd3c-7a4c-4d91-81b1-a73cf54a71d5)
 Call ID: 5e8bbd3c-7a4c-4d91-81b1-a73cf54a71d5
  Args:
    type: :Man
    source: :Foulques_d_Orleans
  AssignClass (d6cda4e3-4a74-4be2-9854-eb4d711764f8)
 Call ID: d6cda4e3-4a74-4be2-9854-eb4d711764f8
  Args:
    source: :Foulques_d_Orleans
    type: :Person
  AddLiteral (fcf6b6aa-8e49-4a66-bb84-18f7edba461d)
 Call ID: fcf6b6aa-8e49-4a66-bb84-18f7edba461d
  Args:
    source: :Foulques_d_Orleans
    relation: :hasBirthYear
    literal_value: 1974
    literal_type: xsd:integer
  AddTriple (1251b880-6e80-443e-928d-f3e89e24ab8d)
 Call ID: 1251b880-6e80-443e-928d-f3e89e24ab8d
  Args:
    relation: :isSonOf
    target: :Jacques_d_Orleans
    source: :Foulques_d_Orleans
  AssignClass (e4e40d9f-4f56-4779-b2cb-5211fa63e572)
 Call ID: e4e40d9f-4f56-4779-b2cb-5211fa63e572
  Args:
    type: :Man
    source: :Francois_d_Orleans_son_of_Henri
  AssignClass (ca5fe7b2-df81-47cc-80af-a2a569908fc9)
 Call ID: ca5fe7b2-df81-47cc-80af-a2a569908fc9
  Args:
    type: :Person
    source: :Francois_d_Orleans_son_of_Henri
  AddTriple (62fea46e-b04f-4b2b-ab11-cbc5e4143178)
 Call ID: 62fea46e-b04f-4b2b-ab11-cbc5e4143178
  Args:
    relation: :isSonOf
    target: :Henri_Philippe_Pierre_Marie_d_Orleans
    source: :Francois_d_Orleans_son_of_Henri
  AssignClass (2239cb03-a694-4850-a4a0-bd88a2a47950)
 Call ID: 2239cb03-a694-4850-a4a0-bd88a2a47950
  Args:
    source: :Jean_d_Orleans
    type: :Man
  AssignClass (fbd55138-99a8-4a5c-b33a-a820180d68ca)
 Call ID: fbd55138-99a8-4a5c-b33a-a820180d68ca
  Args:
    type: :Person
    source: :Jean_d_Orleans
  AddTriple (571fb416-6fff-4bca-b973-d5eaff74567d)
 Call ID: 571fb416-6fff-4bca-b973-d5eaff74567d
  Args:
    relation: :isSonOf
    source: :Jean_d_Orleans
    target: :Henri_Philippe_Pierre_Marie_d_Orleans
  Finish (838a88d9-55d5-49e0-9ae7-aa4dd1266a9c)
 Call ID: 838a88d9-55d5-49e0-9ae7-aa4dd1266a9c
  Args: